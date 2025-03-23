<script>
  import { onMount } from 'svelte';
  import { apiCall } from '$lib/stores/api';

  let originalText = "";
  let wizardTexts = [];
  let selectedIndex = 0;
  let isLoading = false;
  let error = null;

  async function translateText() {
    if (!originalText.trim()) {
      error = "Please enter some text to translate!";
      return;
    }

    error = null;
    isLoading = true;
    wizardTexts = [];
    selectedIndex = 0;
    
    try {
      const response = await apiCall('translate', { text: originalText });
      // Handle the new response format with multiple wizard texts
      wizardTexts = response.wizard_texts || [];
    } catch (err) {
      error = `Translation failed: ${err.message || 'Unknown error'}`;
      console.error(err);
    } finally {
      isLoading = false;
    }
  }

  function selectTranslation(index) {
    selectedIndex = index;
  }

  function copyToClipboard(text) {
    if (!text) return;
    navigator.clipboard.writeText(text);
    alert("Wizard text copied to clipboard!");
  }
</script>

<div class="translator">
  <h2>Wizard Translator</h2>
  <p>Transform your mundane speech into the mystical words of a wizard!</p>
  
  <div class="input-section">
    <label for="original-text">Enter your text:</label>
    <textarea 
      id="original-text" 
      bind:value={originalText} 
      placeholder="Type your ordinary text here..."
      rows="5"
    ></textarea>
    
    <button 
      on:click={translateText} 
      disabled={isLoading || !originalText.trim()} 
      class="translate-btn"
    >
      {isLoading ? 'Conjuring...' : 'Translate to Wizard Speech'}
    </button>
  </div>
  
  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}
  
  {#if wizardTexts.length > 0}
    <div class="output-section">
      <h3>Wizard Translations:</h3>
      
      <div class="translations-container">
        {#each wizardTexts as wizardText, i}
          <div 
            class="wizard-option" 
            class:selected={selectedIndex === i}
            on:click={() => selectTranslation(i)}
          >
            <div class="option-header">
              <h4>Option {i + 1}</h4>
              {#if selectedIndex === i}
                <span class="selected-badge">Selected</span>
              {/if}
            </div>
            <div class="wizard-output">
              <p>{wizardText}</p>
            </div>
            <div class="option-actions">
              <button on:click={() => copyToClipboard(wizardText)} class="copy-btn">
                Copy
              </button>
              <button on:click={() => selectTranslation(i)} class="select-btn">
                {selectedIndex === i ? 'Selected' : 'Select'}
              </button>
            </div>
          </div>
        {/each}
      </div>
      
      {#if selectedIndex !== null && wizardTexts.length > 0}
        <div class="selected-translation">
          <h3>Selected Translation:</h3>
          <div class="wizard-output selected">
            <p>{wizardTexts[selectedIndex]}</p>
          </div>
          <button on:click={() => copyToClipboard(wizardTexts[selectedIndex])} class="copy-btn">
            Copy to Clipboard
          </button>
        </div>
      {/if}
    </div>
  {/if}
</div>

<style>
  .translator {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  h2 {
    color: #9d4edd;
    margin-top: 0;
  }
  
  .input-section, .output-section {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
  }
  
  label {
    font-weight: bold;
    color: #c8b6ff;
  }
  
  textarea {
    padding: 1rem;
    border-radius: 8px;
    border: 2px solid #533483;
    background-color: #1a1a2e;
    color: #e2e2e2;
    font-size: 1rem;
    resize: vertical;
  }
  
  textarea:focus {
    outline: none;
    border-color: #9d4edd;
    box-shadow: 0 0 10px rgba(157, 78, 221, 0.5);
  }
  
  button {
    padding: 0.8rem 1.5rem;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  .translate-btn {
    background-color: #533483;
    color: white;
    border: none;
    align-self: flex-start;
  }
  
  .translate-btn:hover:not(:disabled) {
    background-color: #9d4edd;
    box-shadow: 0 0 15px rgba(157, 78, 221, 0.5);
  }
  
  .translate-btn:disabled {
    background-color: #444;
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .translations-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
  }
  
  .wizard-option {
    border: 2px solid #533483;
    border-radius: 8px;
    padding: 1rem;
    transition: all 0.3s ease;
    cursor: pointer;
  }
  
  .wizard-option:hover {
    border-color: #9d4edd;
    box-shadow: 0 0 10px rgba(157, 78, 221, 0.3);
  }
  
  .wizard-option.selected {
    border-color: #9d4edd;
    background-color: rgba(157, 78, 221, 0.1);
  }
  
  .option-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.5rem;
  }
  
  .option-header h4 {
    margin: 0;
    color: #c8b6ff;
  }
  
  .selected-badge {
    background-color: #9d4edd;
    color: white;
    padding: 0.2rem 0.5rem;
    border-radius: 4px;
    font-size: 0.8rem;
  }
  
  .option-actions {
    display: flex;
    justify-content: flex-end;
    gap: 0.5rem;
    margin-top: 0.8rem;
  }
  
  .wizard-output {
    background-color: #1a1a2e;
    border: 2px solid #9d4edd;
    border-radius: 8px;
    padding: 1.5rem;
    box-shadow: inset 0 0 10px rgba(157, 78, 221, 0.3);
  }
  
  .wizard-output p {
    margin: 0;
    font-style: italic;
    line-height: 1.6;
    color: #c8b6ff;
  }
  
  .selected-translation {
    margin-top: 1.5rem;
    border-top: 1px solid #533483;
    padding-top: 1.5rem;
  }
  
  .copy-btn, .select-btn {
    background-color: #1a1a2e;
    color: #c8b6ff;
    border: 1px solid #533483;
    padding: 0.5rem 1rem;
    font-size: 0.9rem;
  }
  
  .select-btn:hover, .copy-btn:hover {
    background-color: #533483;
    color: white;
  }
  
  .error-message {
    background-color: rgba(220, 53, 69, 0.2);
    border: 1px solid #dc3545;
    color: #ff6b6b;
    padding: 0.8rem;
    border-radius: 8px;
  }
</style>