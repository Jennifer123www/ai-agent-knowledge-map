const MIN_CHINESE_CHARACTERS = 3000;
const MODULE_MAX_CHINESE_CHARACTERS = 5000;

export function validateChineseCharacterCount(count, { independent = false } = {}) {
  if (count < MIN_CHINESE_CHARACTERS || (!independent && count > MODULE_MAX_CHINESE_CHARACTERS)) {
    const range = independent ? `at least ${MIN_CHINESE_CHARACTERS}` : `${MIN_CHINESE_CHARACTERS}-${MODULE_MAX_CHINESE_CHARACTERS}`;
    throw new Error(`Article must contain ${range} Chinese characters (${count})`);
  }
}
