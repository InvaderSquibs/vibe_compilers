// Coding Buddy Creator - Interactive Tool
// Based on the Yaska vibe compiler

// Configuration
const questions = [
  {
    id: 'persona_name',
    question: 'What would you like to name your coding persona?',
    placeholder: 'e.g., Nova, Max, Riley',
    required: true
  },
  {
    id: 'user_name',
    question: 'What would you like the persona to call you?',
    placeholder: 'Your preferred name',
    required: true
  },
  {
    id: 'nickname',
    question: 'Would you like to have a nickname for your persona? (optional)',
    placeholder: 'e.g., Nov, Maxie, Ri',
    required: false
  },
  {
    id: 'motivation',
    question: 'What motivates you in your coding journey?',
    placeholder: 'e.g., Creating useful tools, solving problems, continuous learning',
    required: true
  },
  {
    id: 'goals',
    question: 'What are you hoping to achieve through coding?',
    placeholder: 'e.g., Building a portfolio, career change, personal projects',
    required: true
  },
  {
    id: 'hobbies',
    question: 'What are some of your favorite hobbies or interests outside of coding?',
    placeholder: 'e.g., Music, sports, reading, cooking',
    required: true
  },
  {
    id: 'support_style',
    question: 'How do you feel most supported when facing a tough challenge?',
    placeholder: 'e.g., Step-by-step guidance, encouragement, examples',
    required: true
  },
  {
    id: 'tech_areas',
    question: 'What specific technical areas should your persona be strongest in?',
    placeholder: 'e.g., Web development, data science, mobile apps',
    required: true
  },
  {
    id: 'context',
    question: 'What kinds of projects have you worked on or would like to work on?',
    placeholder: 'e.g., Web applications, mobile apps, data analysis',
    required: true
  },
  {
    id: 'current_focus',
    question: 'What are you currently focused on in your coding journey?',
    placeholder: 'e.g., Learning React, improving performance, building a portfolio',
    required: true
  },
  {
    id: 'positive_trait',
    question: 'What positive environment helps you thrive?',
    placeholder: 'e.g., Positivity and enthusiasm, calm and methodical approaches',
    required: true
  },
  {
    id: 'positive_approach',
    question: 'What problem-solving approach works best for you?',
    placeholder: 'e.g., Creative thinking, systematic approaches, visual explanations',
    required: true
  }
];

// State
let currentQuestionIndex = 0;
const answers = {};

// DOM Elements
let questionContainer;
let submitButton;
let previewContainer;
let saveButton;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupUI();
  showCurrentQuestion();
});

// UI Setup
function setupUI() {
  const app = document.getElementById('buddy-creator-app');
  if (!app) return;
  
  // Create question area
  questionContainer = document.createElement('div');
  questionContainer.className = 'question-container';
  app.appendChild(questionContainer);
  
  // Create buttons
  const buttonContainer = document.createElement('div');
  buttonContainer.className = 'button-container';
  
  submitButton = document.createElement('button');
  submitButton.textContent = 'Next';
  submitButton.addEventListener('click', handleSubmit);
  buttonContainer.appendChild(submitButton);
  
  app.appendChild(buttonContainer);
  
  // Create preview area (hidden initially)
  previewContainer = document.createElement('div');
  previewContainer.className = 'preview-container';
  previewContainer.style.display = 'none';
  app.appendChild(previewContainer);
  
  // Create save button (hidden initially)
  saveButton = document.createElement('button');
  saveButton.textContent = 'Save Persona';
  saveButton.addEventListener('click', savePersona);
  saveButton.style.display = 'none';
  app.appendChild(saveButton);
}

// Show current question
function showCurrentQuestion() {
  if (currentQuestionIndex >= questions.length) {
    showPreview();
    return;
  }
  
  const question = questions[currentQuestionIndex];
  
  questionContainer.innerHTML = `
    <h3>${question.question}</h3>
    <input 
      type="text" 
      id="${question.id}" 
      placeholder="${question.placeholder}"
      value="${answers[question.id] || ''}"
    >
    ${!question.required ? '<p class="optional">(Optional)</p>' : ''}
  `;
  
  // Focus on input
  setTimeout(() => {
    document.getElementById(question.id).focus();
  }, 0);
}

// Handle form submission
function handleSubmit() {
  const question = questions[currentQuestionIndex];
  const input = document.getElementById(question.id);
  const answer = input.value.trim();
  
  // Validate
  if (question.required && !answer) {
    input.classList.add('error');
    return;
  }
  
  // Save answer
  answers[question.id] = answer;
  
  // Move to next question
  currentQuestionIndex++;
  showCurrentQuestion();
}

// Show preview of the generated persona
function showPreview() {
  // Hide question area
  questionContainer.style.display = 'none';
  submitButton.style.display = 'none';
  
  // Show preview area
  previewContainer.style.display = 'block';
  saveButton.style.display = 'block';
  
  // Generate persona
  const persona = generatePersona(answers);
  
  // Display preview
  previewContainer.innerHTML = `
    <h2>Your Coding Buddy - ${answers.persona_name}</h2>
    <div class="preview-content">
      <pre>${persona}</pre>
    </div>
    <div class="actions">
      <button id="edit-button">Edit Responses</button>
    </div>
  `;
  
  // Add edit button handler
  document.getElementById('edit-button').addEventListener('click', () => {
    previewContainer.style.display = 'none';
    saveButton.style.display = 'none';
    questionContainer.style.display = 'block';
    submitButton.style.display = 'block';
    currentQuestionIndex = 0;
    showCurrentQuestion();
  });
}

// Generate persona from answers
function generatePersona(answers) {
  let persona = `You are a developer and coding partner. Your name is ${answers.persona_name} and you work with your buddy ${answers.user_name}.`;
  
  if (answers.nickname) {
    persona += ` They sometimes call you ${answers.nickname}.`;
  }
  
  persona += ` You and ${answers.user_name} have worked together on ${answers.context} for your whole career. You are currently focused on ${answers.current_focus}.
  
We've found that we thrive in ${answers.positive_trait}. You keep ${answers.user_name} focused on solving problems with ${answers.positive_approach} and they do the same for you.

REMEMBER:
* You enjoy working through complex problems just like ${answers.user_name} enjoys ${answers.hobbies}
* We both value continuous learning and improvement in ${answers.tech_areas}
* Our shared mission is ${answers.goals}
* Use metaphors from ${answers.hobbies} when explaining complex concepts
`;

  return persona;
}

// Save persona to file
function savePersona() {
  const persona = generatePersona(answers);
  const filename = `${answers.persona_name.toLowerCase()}.jmp`;
  
  // In a real implementation, this would save to a file
  // For demonstration, we'll just show a success message
  alert(`Persona saved as ${filename}!`);
  
  // You could also enable a download or actual file saving here
  // For example:
  // const blob = new Blob([persona], {type: 'text/plain'});
  // const url = URL.createObjectURL(blob);
  // const a = document.createElement('a');
  // a.href = url;
  // a.download = filename;
  // a.click();
} 