<script lang="ts">
  import Translator from '$lib/components/Translator.svelte';
  import Judge from '$lib/components/Judge.svelte';
  
  let activeTab = 'translator'; // Default to translator view
</script>

<main>
  <div class="wizard-app">
    <header>
      <h1>Wizard Speech Trainer</h1>
      <div class="tabs">
        <button 
          class:active={activeTab === 'translator'} 
          on:click={() => activeTab = 'translator'}>
          Wizard Translator
        </button>
        <button 
          class:active={activeTab === 'judge'} 
          on:click={() => activeTab = 'judge'}>
          Wizard Judge
        </button>
      </div>
    </header>
    
    <div class="content">
      {#if activeTab === 'translator'}
        <Translator />
      {:else if activeTab === 'judge'}
        <Judge />
      {/if}
    </div>
  </div>
</main>

<style>
  :global(body) {
    background-color: #1a1a2e;
    color: #e2e2e2;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    margin: 0;
    padding: 0;
  }
  
  .wizard-app {
    max-width: 800px;
    margin: 0 auto;
    padding: 2rem;
  }
  
  header {
    text-align: center;
    margin-bottom: 2rem;
  }
  
  h1 {
    color: #9d4edd;
    font-size: 2.5rem;
    margin-bottom: 1rem;
    text-shadow: 0 0 10px rgba(157, 78, 221, 0.4);
  }
  
  .tabs {
    display: flex;
    justify-content: center;
    margin-bottom: 1rem;
    gap: 1rem;
  }
  
  button {
    background-color: #16213e;
    color: #e2e2e2;
    border: 2px solid #533483;
    border-radius: 8px;
    padding: 0.5rem 1.5rem;
    font-size: 1rem;
    cursor: pointer;
    transition: all 0.3s ease;
  }
  
  button:hover {
    background-color: #533483;
  }
  
  button.active {
    background-color: #533483;
    border-color: #9d4edd;
    box-shadow: 0 0 15px rgba(157, 78, 221, 0.5);
  }
  
  .content {
    background-color: #16213e;
    border-radius: 12px;
    padding: 2rem;
    box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  }
</style>
