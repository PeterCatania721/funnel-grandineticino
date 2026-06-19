/**
 * Prefisso telefonico con dropdown bandiera + numero locale.
 * Valida la parte locale in base al prefisso selezionato.
 */
(function () {
  'use strict';

  var DIAL_CODES = [
    { code: '+423', flag: '🇱🇮' },
    { code: '+41', flag: '🇨🇭' },
    { code: '+39', flag: '🇮🇹' },
    { code: '+49', flag: '🇩🇪' },
    { code: '+33', flag: '🇫🇷' },
    { code: '+43', flag: '🇦🇹' },
    { code: '+44', flag: '🇬🇧' },
    { code: '+1', flag: '🇺🇸' },
  ];

  var LOCAL_DIGIT_RULES = {
    '+41': { min: 9, max: 9 },
    '+39': { min: 9, max: 10 },
    '+49': { min: 10, max: 11 },
    '+33': { min: 9, max: 9 },
    '+43': { min: 10, max: 13 },
    '+423': { min: 7, max: 9 },
    '+44': { min: 10, max: 10 },
    '+1': { min: 10, max: 10 },
  };

  var DEFAULT_RULES = { min: 8, max: 12 };
  var STRIP_TRUNK_ZERO = { '+41': 1, '+39': 1, '+43': 1, '+49': 1, '+33': 1, '+423': 1 };

  function splitPhoneValue(value) {
    var trimmed = (value || '').trim();
    if (!trimmed) {
      return { code: '+41', local: '' };
    }

    var normalized = trimmed.replace(/\s+/g, '');
    if (normalized.charAt(0) !== '+') {
      return { code: '+41', local: trimmed };
    }

    for (var i = 0; i < DIAL_CODES.length; i += 1) {
      var code = DIAL_CODES[i].code;
      if (normalized.indexOf(code) === 0) {
        return {
          code: code,
          local: trimmed.slice(trimmed.indexOf(code) + code.length).trim(),
        };
      }
    }

    return { code: '+41', local: trimmed };
  }

  function getLocalNumber(input) {
    var local = (input.dataset.telLocal || input.value || '').trim();
    if (local.charAt(0) === '+') {
      return splitPhoneValue(local).local;
    }
    return local;
  }

  function normalizeLocalDigits(local, code) {
    var digits = (local || '').replace(/\D/g, '');
    if (STRIP_TRUNK_ZERO[code] && digits.charAt(0) === '0') {
      digits = digits.slice(1);
    }
    return digits;
  }

  function getTelFullValue(wrap) {
    var select = wrap.querySelector('.prev-tel-country-select');
    var input = wrap.querySelector('.prev-input--tel');
    if (!select || !input) return '';

    var local = getLocalNumber(input).trim();
    if (!local) return '';
    if (local.charAt(0) === '+') return local;
    return select.value + ' ' + local;
  }

  function validateTelWrap(wrap) {
    var select = wrap.querySelector('.prev-tel-country-select');
    var input = wrap.querySelector('.prev-input--tel');
    if (!select || !input) return false;

    var local = getLocalNumber(input);
    if (!local) return false;

    var code = select.value;
    var digits = normalizeLocalDigits(local, code);
    if (!digits) return false;
    if (digits.charAt(0) === '0') return false;

    var rules = LOCAL_DIGIT_RULES[code] || DEFAULT_RULES;
    return digits.length >= rules.min && digits.length <= rules.max;
  }

  function isTelWrapEmpty(wrap) {
    return !getLocalNumber(wrap.querySelector('.prev-input--tel')).trim();
  }

  function syncWrap(wrap) {
    var input = wrap.querySelector('.prev-input--tel');
    if (!input) return;
    input.value = getTelFullValue(wrap);
  }

  function bindWrap(wrap) {
    if (wrap.dataset.telPrefixInit) return;
    wrap.dataset.telPrefixInit = '1';

    var select = wrap.querySelector('.prev-tel-country-select');
    var input = wrap.querySelector('.prev-input--tel');
    if (!select || !input) return;

    var split = splitPhoneValue(input.value);
    select.value = split.code;
    input.value = split.local;
    input.dataset.telLocal = split.local;

    function rememberLocal() {
      var local = input.value.trim();
      if (local.charAt(0) === '+') {
        split = splitPhoneValue(local);
        select.value = split.code;
        local = split.local;
        input.value = local;
      }
      input.dataset.telLocal = local;
    }

    input.addEventListener('input', rememberLocal);
    input.addEventListener('change', rememberLocal);
    input.addEventListener('blur', rememberLocal);

    select.addEventListener('change', function () {
      rememberLocal();
      input.focus();
    });

    var form = wrap.closest('form');
    if (form && !form.dataset.telPrefixSubmit) {
      form.dataset.telPrefixSubmit = '1';
      form.addEventListener('submit', function () {
        form.querySelectorAll('[data-tel-prefix]').forEach(syncWrap);
      });
    }
  }

  function initTelPrefix(root) {
    (root || document).querySelectorAll('[data-tel-prefix]').forEach(bindWrap);
  }

  window.validateTelWrap = validateTelWrap;
  window.isTelWrapEmpty = isTelWrapEmpty;
  window.syncTelPrefixFields = function (root) {
    (root || document).querySelectorAll('[data-tel-prefix]').forEach(syncWrap);
  };

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { initTelPrefix(); });
  } else {
    initTelPrefix();
  }
})();
