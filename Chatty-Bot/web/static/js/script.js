const triggerList = document.querySelector('.trigger-list');
const triggerInput = document.getElementById('trigger');
const responseInput = document.getElementById('response');
const languageSelect = document.getElementById('language');

// Function to fetch triggers from backend and display in the admin panel
async function fetchAndDisplayTriggers(language) {
  const url = `/triggers?language=${language}`;

  try {
    const response = await fetch(url);
    const data = await response.json();

    if (data && data.triggers) {
      // Clear existing trigger list
      triggerList.innerHTML = '';

      // Display fetched triggers
      data.triggers.forEach(trigger => {
        const listItem = document.createElement('li');
        listItem.textContent = `${trigger.trigger} - ${trigger.response}`;

        // Add click event to select trigger for update/delete
        listItem.addEventListener('click', () => {
          selectedTriggerId = trigger._id;
          triggerInput.value = trigger.trigger;
          responseInput.value = trigger.response;
        });

        triggerList.appendChild(listItem);
      });
    }
  } catch (error) {
    console.error('Error fetching triggers:', error);
  }
}

// Call the function to fetch and display triggers when the admin panel loads
window.onload = function () {
  languageSelect.addEventListener('change', function () {
    const selectedLanguage = languageSelect.value;
    fetchAndDisplayTriggers(selectedLanguage);
  });

  // Fetch triggers on page load with default language
  const defaultLanguage = languageSelect.value;
  fetchAndDisplayTriggers(defaultLanguage);
};

// Function to add a new trigger
function addTrigger() {
  const trigger = {
    trigger: triggerInput.value.trim(),
    response: responseInput.value.trim(),
    language: languageSelect.value,  // Get the selected language
  };

  if (!trigger.trigger || !trigger.response) {
    console.error('Please enter both trigger and response');
    return;
  }

  fetch('/add_trigger', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(trigger),
  })
  .then(response => {
    if (response.ok) {
      return response.json();
    }
    throw new Error('Failed to add trigger');
  })
  .then(data => {
    console.log(data.message);
    // Refresh trigger list after adding
    fetchAndDisplayTriggers(trigger.language);
    // Clear input fields after adding
    triggerInput.value = '';
    responseInput.value = '';
  })
  .catch(error => {
    console.error('Error:', error);
  });
}
