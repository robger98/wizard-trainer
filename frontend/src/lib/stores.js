import { writable } from 'svelte/store';

// Update store to handle multiple translations
export const createTranslationStore = () => {
  const { subscribe, set, update } = writable({
    original: '',
    translations: [],
    selectedTranslation: null
  });
  
  return {
    subscribe,
    setTranslations: (original, translations) => {
      set({
        original,
        translations,
        selectedTranslation: translations[0] // Default to first translation
      });
    },
    selectTranslation: (index) => {
      update(state => ({
        ...state,
        selectedTranslation: state.translations[index]
      }));
    },
    reset: () => set({ original: '', translations: [], selectedTranslation: null })
  };
};