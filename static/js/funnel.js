/**
 * Grandineticino.ch — multi-step form, upload foto + mobile UX.
 */
(function () {
  'use strict';

  var MAX_BYTES = 20 * 1024 * 1024;
  var ALLOWED_IMAGE_EXTS = {
    jpg: 1, jpeg: 1, jfif: 1, pjpeg: 1, pjp: 1,
    png: 1, gif: 1, webp: 1, heic: 1, heif: 1,
    bmp: 1, tif: 1, tiff: 1, avif: 1
  };

  var STEP_LABELS = (window.FUNNEL_I18N && window.FUNNEL_I18N.stepLabels) || ['Contatto', 'Foto', 'Invio'];
  var I18N = window.FUNNEL_I18N || {};

  function isAllowedImageFile(file) {
    if (!file) return false;
    var type = (file.type || '').toLowerCase();
    if (type.indexOf('image/') === 0) return true;
    var name = file.name || '';
    var dot = name.lastIndexOf('.');
    if (dot < 0) return false;
    var ext = name.slice(dot + 1).toLowerCase();
    return !!ALLOWED_IMAGE_EXTS[ext];
  }

  function trimFieldValue(field) {
    if (!field || field.type === 'checkbox' || field.type === 'file') return;
    if (typeof field.value === 'string') field.value = field.value.trim();
  }

  function isTextField(field) {
    if (!field) return false;
    var tag = (field.tagName || '').toLowerCase();
    return tag === 'textarea' || field.type === 'text' || field.type === 'email' || field.type === 'tel' || field.type === 'textarea';
  }

  function fieldValue(field) {
    return String(field && field.value != null ? field.value : '').trim();
  }

  function isValidEmail(value) {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
  }

  function fieldMessage(name, fallback) {
    var map = {
      email: I18N.invalidEmail || I18N.requiredFields,
      telephone: I18N.invalidPhone,
      city: I18N.requiredFields,
      delivery_preference: I18N.selectDelivery || I18N.requiredFields,
      damage_details: I18N.requiredFields,
      images: I18N.uploadRequired,
      terms: I18N.acceptTerms,
    };
    return map[name] || fallback || I18N.requiredFields || 'Compila tutti i campi obbligatori.';
  }

  function markFieldInvalid(field, invalid) {
    if (!field) return;
    field.classList.toggle('is-invalid', invalid);
    var wrap = field.closest('.prev-tel-wrap');
    if (wrap) wrap.classList.toggle('is-invalid', invalid);
    var upload = field.closest('.prev-field') && field.closest('.prev-field').querySelector('.prev-upload');
    if (upload) upload.classList.toggle('is-invalid', invalid);
    var checkField = field.closest('.prev-field--check');
    if (checkField) checkField.classList.toggle('is-invalid', invalid);
  }

  window.funnelFormWizard = function () {
    return {
      step: 1,
      totalSteps: 3,
      stepError: '',
      fieldErrors: {},
      errorSteps: {},

      formEl: function () {
        return this.$root || this.$el;
      },

      init: function () {
        var self = this;
        var form = this.formEl();
        form.__funnelSyncHeight = function () { self.syncPanelHeight(); };
        form.addEventListener('funnel:panels-resize', form.__funnelSyncHeight);
        this.restoreServerErrors();
        this.bindFieldClear();
        this.$nextTick(function () {
          self.syncPanelHeight();
          if (Object.keys(self.fieldErrors).length) {
            self.scrollToFirstError();
          }
        });
        if (!window._funnelPanelResize) {
          window._funnelPanelResize = true;
          window.addEventListener('resize', function () {
            document.querySelectorAll('form.funnel-form').forEach(function (el) {
              if (typeof el.__funnelSyncHeight === 'function') {
                el.__funnelSyncHeight();
              }
            });
          });
        }
      },

      syncPanelHeight: function () {
        var wrap = this.$refs.panels;
        if (!wrap || wrap.closest('.funnel-hero-form-wrap--prominent')) return;
        var panels = wrap.querySelectorAll('.funnel-form-panel');
        var max = 0;

        panels.forEach(function (panel) {
          panel.dataset.funnelMeasure = '1';
          panel.style.setProperty('display', 'block', 'important');
          panel.style.visibility = 'hidden';
          panel.style.position = 'absolute';
          panel.style.inset = '0 auto auto 0';
          panel.style.width = '100%';
          panel.style.pointerEvents = 'none';
          max = Math.max(max, panel.scrollHeight);
        });

        panels.forEach(function (panel) {
          delete panel.dataset.funnelMeasure;
          panel.style.removeProperty('display');
          panel.style.visibility = '';
          panel.style.position = '';
          panel.style.inset = '';
          panel.style.width = '';
          panel.style.pointerEvents = '';
        });

        wrap.style.minHeight = max + 'px';
      },
      stepLabel: function (n) {
        return STEP_LABELS[n - 1] || '';
      },

      stepHasError: function (n) {
        return !!this.errorSteps[n];
      },

      clearFieldError: function (name) {
        if (!name || !this.fieldErrors[name]) return;
        delete this.fieldErrors[name];
        this.refreshErrorSteps();
        if (!Object.keys(this.fieldErrors).length) {
          this.stepError = '';
        }
      },

      refreshErrorSteps: function () {
        var steps = {};
        var form = this.formEl();
        Object.keys(this.fieldErrors).forEach(function (name) {
          var field = form.querySelector('[name="' + name + '"]');
          if (!field) return;
          var panel = field.closest('[data-funnel-step]');
          if (panel) steps[panel.getAttribute('data-funnel-step')] = true;
        });
        this.errorSteps = steps;
      },

      setFieldError: function (name, message, field) {
        this.fieldErrors[name] = message;
        this.stepError = message;
        this.refreshErrorSteps();
        markFieldInvalid(field, true);
        if (field && field.id) {
          field.setAttribute('aria-invalid', 'true');
          field.setAttribute('aria-describedby', field.id + '-error');
        }
      },

      clearPanelErrors: function (panel) {
        if (!panel) return;
        panel.querySelectorAll('.is-invalid').forEach(function (el) {
          el.classList.remove('is-invalid');
        });
        panel.querySelectorAll('[aria-invalid="true"]').forEach(function (el) {
          el.removeAttribute('aria-invalid');
          el.removeAttribute('aria-describedby');
        });
      },

      restoreServerErrors: function () {
        var raw = this.formEl().getAttribute('data-funnel-server-state');
        if (!raw) return;
        try {
          var data = JSON.parse(raw);
          if (!data || !data.fields) return;
          this.fieldErrors = Object.assign({}, data.fields);
          if (data.step) this.step = parseInt(data.step, 10) || 1;
          var firstMessage = Object.values(this.fieldErrors)[0];
          if (firstMessage) this.stepError = firstMessage;
          this.refreshErrorSteps();
          var self = this;
          Object.keys(this.fieldErrors).forEach(function (name) {
            var field = self.formEl().querySelector('[name="' + name + '"]');
            markFieldInvalid(field, true);
            if (field && field.id) {
              field.setAttribute('aria-invalid', 'true');
              field.setAttribute('aria-describedby', field.id + '-error');
            }
          });
        } catch (e) {
          /* ignore malformed server state */
        }
      },

      bindFieldClear: function () {
        var self = this;
        this.formEl().querySelectorAll('input, select, textarea').forEach(function (field) {
          if (!field.name) return;
          var eventName = field.type === 'checkbox' || field.tagName === 'SELECT' ? 'change' : 'input';
          field.addEventListener(eventName, function () {
            if (!self.fieldErrors[field.name]) return;
            delete self.fieldErrors[field.name];
            markFieldInvalid(field, false);
            field.removeAttribute('aria-invalid');
            field.removeAttribute('aria-describedby');
            self.refreshErrorSteps();
            if (!Object.keys(self.fieldErrors).length) {
              self.stepError = '';
            }
          });
        });
      },

      scrollToFirstError: function () {
        var form = this.formEl();
        var panel = form.querySelector('[data-funnel-step="' + this.step + '"]');
        if (!panel) return;

        var target = panel.querySelector('.is-invalid, [aria-invalid="true"]');
        if (!target) {
          target = form.querySelector('.funnel-form-step-error.is-visible') || panel;
        }

        /* Form hero: scroll solo dentro il pannello, non tutta la pagina */
        if (form.closest('.funnel-hero-form-wrap--prominent')) {
          var scrollParent = form.querySelector('.funnel-form-panels');
          if (scrollParent && target && panel.contains(target)) {
            var panelRect = panel.getBoundingClientRect();
            var targetRect = target.getBoundingClientRect();
            var delta = targetRect.top - panelRect.top - 16;
            scrollParent.scrollTop += delta;
          }
          return;
        }

        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      },

      goNext: function () {
        if (!this.validateStep(this.step)) {
          this.scrollToFirstError();
          return;
        }
        this.stepError = '';
        if (this.step < this.totalSteps) {
          this.step += 1;
          this.afterStepChange();
        }
      },

      goBack: function () {
        this.stepError = '';
        if (this.step > 1) {
          this.step -= 1;
          this.afterStepChange();
        }
      },

      afterStepChange: function () {
        var self = this;
        this.$nextTick(function () {
          self.syncPanelHeight();
          self.focusStep();
        });
      },

      onSubmit: function (e) {
        var self = this;
        if (window.syncTelPrefixFields) {
          window.syncTelPrefixFields(this.formEl());
        }

        if (this.step !== this.totalSteps) {
          e.preventDefault();
          return;
        }

        var stepsOrder = [this.step];
        for (var s = 1; s <= this.totalSteps; s += 1) {
          if (stepsOrder.indexOf(s) === -1) stepsOrder.push(s);
        }

        for (var i = 0; i < stepsOrder.length; i += 1) {
          if (!this.validateStep(stepsOrder[i], false)) {
            e.preventDefault();
            this.step = stepsOrder[i];
            this.afterStepChange();
            this.$nextTick(function () {
              self.scrollToFirstError();
            });
            return;
          }
        }
      },

      focusStep: function () {
        var self = this;
        var root = this.formEl();
        requestAnimationFrame(function () {
          var panel = root.querySelector('[data-funnel-step="' + self.step + '"]');
          if (!panel) return;
          var field = panel.querySelector('input:not([type="hidden"]):not([type="file"]), select, textarea');
          if (field) field.focus({ preventScroll: true });
        });
      },

      validateStep: function (stepNum, silent) {
        var panel = this.formEl().querySelector('[data-funnel-step="' + stepNum + '"]');
        if (!panel) return false;

        this.clearPanelErrors(panel);
        Object.keys(this.fieldErrors).forEach(function (name) {
          var field = panel.querySelector('[name="' + name + '"]');
          if (field) delete this.fieldErrors[name];
        }, this);
        this.refreshErrorSteps();
        if (!Object.keys(this.fieldErrors).length) {
          this.stepError = '';
        }

        var fields = panel.querySelectorAll('input, select, textarea');
        var self = this;

        function fail(name, message, field) {
          if (!silent) {
            self.setFieldError(name, message, field);
            if (field) {
              field.focus({ preventScroll: true });
            }
          }
          return false;
        }

        for (var i = 0; i < fields.length; i++) {
          var field = fields[i];

          if (field.classList.contains('prev-tel-country-select')) {
            continue;
          }

          if (isTextField(field)) {
            trimFieldValue(field);
          }

          var name = field.name;
          if (!name) continue;

          if (field.type === 'checkbox') {
            if (field.required && !field.checked) {
              return fail(name, fieldMessage('terms'), field);
            }
            continue;
          }

          if (field.type === 'file') {
            if (field.hasAttribute('data-funnel-required') && (!field.files || field.files.length === 0)) {
              return fail(name, fieldMessage('images'), field);
            }
            continue;
          }

          if (field.classList.contains('prev-input--tel')) {
            var telWrap = field.closest('[data-tel-prefix]');
            if (field.required && window.isTelWrapEmpty && window.isTelWrapEmpty(telWrap)) {
              return fail(name, I18N.requiredFields || fieldMessage('telephone'), field);
            }
            if (field.required && window.validateTelWrap && !window.validateTelWrap(telWrap)) {
              return fail(name, fieldMessage('telephone'), field);
            }
            continue;
          }

          if (name === 'email' || field.type === 'email') {
            var emailValue = fieldValue(field);
            if (field.required && !emailValue) {
              return fail(name, I18N.requiredFields || fieldMessage('email'), field);
            }
            if (emailValue && !isValidEmail(emailValue)) {
              return fail(name, I18N.invalidEmail || fieldMessage('email'), field);
            }
            continue;
          }

          if (name === 'delivery_preference') {
            if (field.required && !fieldValue(field)) {
              return fail(name, fieldMessage('delivery_preference'), field);
            }
            continue;
          }

          if (field.required && !fieldValue(field)) {
            return fail(name, fieldMessage(name), field);
          }
        }

        delete this.errorSteps[String(stepNum)];
        return true;
      }
    };
  };

  function initFunnelForms() {
    document.querySelectorAll('.funnel-form').forEach(function (form) {
      if (form.dataset.funnelUploadInit) return;
      form.dataset.funnelUploadInit = '1';

      var input = form.querySelector('.funnel-upload-input');
      var grid = form.querySelector('.funnel-preview-grid');
      var submit = form.querySelector('button[type="submit"]');
      if (!input || !grid || !submit) return;

      var files = [];

      input.addEventListener('change', function () {
        var rejected = 0;
        Array.from(this.files).forEach(function (f) {
          if (!isAllowedImageFile(f)) {
            rejected += 1;
            return;
          }
          if (files.length < 15) files.push(f);
        });
        if (rejected > 0) {
          var msg = I18N.uploadInvalidType ||
            'Formato file non supportato. Carica solo immagini (JPG, PNG, HEIC, WebP, GIF, …).';
          window.alert(msg);
        }
        syncInput();
        render();
      });

      form.addEventListener('submit', function (e) {
        if (totalBytes() > MAX_BYTES) e.preventDefault();
      });

      function totalBytes() {
        return files.reduce(function (sum, f) { return sum + f.size; }, 0);
      }

      function fmtSize(bytes) {
        if (bytes >= 1024 * 1024) return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
        return Math.round(bytes / 1024) + ' KB';
      }

      function syncInput() {
        var dt = new DataTransfer();
        files.forEach(function (f) { dt.items.add(f); });
        input.files = dt.files;
        input.required = files.length === 0;
      }

      function render() {
        grid.innerHTML = '';
        grid.hidden = files.length === 0;
        var total = totalBytes();
        var overLimit = total > MAX_BYTES;

        if (files.length > 0) {
          var bar = document.createElement('div');
          bar.className = 'prev-size-bar' + (overLimit ? ' prev-size-bar--over' : '');
          var pct = Math.min(total / MAX_BYTES * 100, 100);
          bar.innerHTML =
            '<div class="prev-size-track"><div class="prev-size-fill" style="width:' + pct + '%"></div></div>' +
            '<span class="prev-size-label">' + fmtSize(total) + ' / 20 MB</span>';

          if (overLimit) {
            var warn = document.createElement('p');
            warn.className = 'prev-size-warning';
            warn.textContent = I18N.uploadTooLarge || 'Totale allegati troppo grande per l\'invio via email. Rimuovi alcuni file fino a tornare sotto i 20 MB.';
            bar.appendChild(warn);
          }

          grid.appendChild(bar);
          submit.disabled = overLimit;
          submit.style.opacity = overLimit ? '0.45' : '';
          submit.style.cursor = overLimit ? 'not-allowed' : '';
        } else {
          submit.disabled = false;
          submit.style.opacity = '';
          submit.style.cursor = '';
        }

        files.forEach(function (f, idx) {
          var item = document.createElement('div');
          item.className = 'prev-preview-item';

          if (f.type.startsWith('image/')) {
            var img = document.createElement('img');
            img.className = 'prev-preview-thumb';
            img.alt = f.name;
            var reader = new FileReader();
            reader.onload = function (e) { img.src = e.target.result; };
            reader.readAsDataURL(f);
            item.appendChild(img);
          } else {
            var icon = document.createElement('div');
            icon.className = 'prev-preview-icon';
            icon.textContent = f.name.split('.').pop().toUpperCase();
            item.appendChild(icon);
          }

          var name = document.createElement('span');
          name.className = 'prev-preview-name';
          name.textContent = f.name;
          item.appendChild(name);

          var size = document.createElement('span');
          size.className = 'prev-preview-size';
          size.textContent = fmtSize(f.size);
          item.appendChild(size);

          var btn = document.createElement('button');
          btn.type = 'button';
          btn.className = 'prev-preview-del';
          btn.setAttribute('aria-label', (I18N.removeFile || 'Rimuovi') + ' ' + f.name);
          btn.innerHTML = '&times;';
          btn.addEventListener('click', function () {
            files.splice(idx, 1);
            syncInput();
            render();
          });
          item.appendChild(btn);
          grid.appendChild(item);
        });
        form.dispatchEvent(new CustomEvent('funnel:panels-resize'));
      }
    });
  }

  function initFunnelAnchors() {
    document.querySelectorAll('a[href^="#"]').forEach(function (link) {
      if (link.dataset.funnelAnchorInit) return;
      link.dataset.funnelAnchorInit = '1';
      link.addEventListener('click', function (e) {
        var hash = this.getAttribute('href');
        if (!hash || hash.length < 2) return;
        var target = document.getElementById(hash.slice(1));
        if (!target) return;
        e.preventDefault();
        var header = document.querySelector('.funnel-header');
        var offset = header ? header.offsetHeight + 12 : 72;
        var top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top: Math.max(0, top), behavior: 'smooth' });
      });
    });
  }

  function bootFunnelDom() {
    initFunnelAnchors();
    initFunnelForms();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootFunnelDom);
  } else {
    bootFunnelDom();
  }
})();
