<script>
  import { apiCall } from '$lib/stores/api';

  let userText = "";
  let judgement = null;
  let isLoading = false;
  let error = null;

  async function judgeText() {
    if (!userText.trim()) {
      error = "Please enter some text to judge!";
      return;
    }

    error = null;
    isLoading = true;
    
    try {
      judgement = await apiCall('judge', { text: userText });
    } catch (err) {
      error = `Judgement failed: ${err.message || 'Unknown error'}`;
      console.error(err);
    } finally {
      isLoading = false;
    }
  }

  function getScoreColor(score) {
    if (score <= 3) return "#ff6b6b";
    if (score <= 6) return "#ffd166";
    return "#06d6a0";
  }
</script>

<div class="judge">
  <h2>Wizard Speech Judge</h2>
  <p>Test your wizardly speaking abilities and receive feedback!</p>
  
  <div class="input-section">
    <label for="judge-text">Enter your wizard speech:</label>
    <textarea 
      id="judge-text" 
      bind:value={userText} 
      placeholder="Write in your most wizardly voice..."
      rows="5"
    ></textarea>
    
    <button 
      on:click={judgeText} 
      disabled={isLoading || !userText.trim()} 
      class="judge-btn"
    >
      {isLoading ? 'Divining...' : 'Judge My Wizardly Speech'}
    </button>
  </div>
  
  {#if error}
    <div class="error-message">
      {error}
    </div>
  {/if}
  
  {#if judgement}
    <div class="judgement-section">
      <h3>The Wizard Council's Verdict:</h3>
      
      <div class="score-section">
        <div class="score-container">
          <div class="score" style="color: {getScoreColor(judgement.score)}">
            {judgement.score}
          </div>
          <div class="score-label">
            out of 10
          </div>
        </div>
        
        <div class="feedback">
          <p>{judgement.feedback}</p>
        </div>
      </div>
      
      <div class="suggestions">
        <h4>Wizardly Suggestions:</h4>
        <ul>
          {#each judgement.suggestions as suggestion}
            <li>{suggestion}</li>
          {/each}
        </ul>
      </div>
    </div>
  {/if}
</div>

<style>
  .judge {
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
  }
  
  h2 {
    color: #9d4edd;
    margin-top: 0;
  }
  
  .input-section {
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
  
  .judge-btn {
    background-color: #533483;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.8rem 1.5rem;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    align-self: flex-start;
  }
  
  .judge-btn:hover:not(:disabled) {
    background-color: #9d4edd;
    box-shadow: 0 0 15px rgba(157, 78, 221, 0.5);
  }
  
  .judge-btn:disabled {
    background-color: #444;
    cursor: not-allowed;
    opacity: 0.6;
  }
  
  .judgement-section {
    background-color: #1a1a2e;
    border: 2px solid #9d4edd;
    border-radius: 8px;
    padding: 1.5rem;
  }
  
  .score-section {
    display: flex;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1.5rem;
  }
  
  .score-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    min-width: 100px;
  }
  
  .score {
    font-size: 3.5rem;
    font-weight: bold;
  }
  
  .score-label {
    font-size: 0.9rem;
    opacity: 0.8;
  }
  
  .feedback {
    flex: 1;
    border-left: 1px solid #533483;
    padding-left: 2rem;
  }
  
  .feedback p {
    margin: 0;
    font-size: 1.1rem;
    line-height: 1.6;
    font-style: italic;
  }
  
  .suggestions h4 {
    color: #c8b6ff;
    margin-bottom: 0.8rem;
  }
  
  .suggestions ul {
    margin: 0;
    padding-left: 1.5rem;
  }
  
  .suggestions li {
    margin-bottom: 0.5rem;
  }
  
  .error-message {
    background-color: rgba(220, 53, 69, 0.2);
    border: 1px solid #dc3545;
    color: #ff6b6b;
    padding: 0.8rem;
    border-radius: 8px;
  }
</style>