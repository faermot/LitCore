(function () {
  'use strict';

  var CONFIGS = {
    id_photo: { ratio: 1 / 1,  label: 'фото автора (1:1)' },
    id_cover: { ratio: 2 / 3,  label: 'обложки книги (2:3)' },
    id_image: { ratio: 3 / 1,  label: 'баннера жанра (3:1)' },
  };

  function clamp(v, lo, hi) { return Math.max(lo, Math.min(hi, v)); }

  function buildCropper(inputEl, cfg) {
    var cropField = document.getElementById('id_crop_data');
    if (!cropField) return;

    var wrapper, canvas, overlay, hint;
    var state = { dragging: false, sx: 0, sy: 0, x: 0, y: 0, w: 0, h: 0 };
    var imgObj = new Image();
    var dispW = 0, dispH = 0;

    inputEl.addEventListener('change', function () {
      cropField.value = '';
      if (wrapper) { wrapper.remove(); wrapper = null; }
      if (hint) { hint.remove(); hint = null; }

      var file = inputEl.files[0];
      if (!file) return;

      hint = document.createElement('p');
      hint.style.cssText = 'margin:10px 0 6px;font-size:12px;color:#555;';
      hint.textContent = 'Выделите область для обрезки ' + cfg.label + ':';
      inputEl.parentNode.insertBefore(hint, inputEl.nextSibling);

      wrapper = document.createElement('div');
      wrapper.style.cssText = 'position:relative;display:inline-block;'
        + 'margin-top:4px;cursor:crosshair;user-select:none;'
        + 'border:2px solid #ddd;border-radius:4px;overflow:hidden;'
        + 'max-width:400px;';

      canvas = document.createElement('canvas');
      canvas.style.cssText = 'display:block;max-width:400px;';

      overlay = document.createElement('canvas');
      overlay.style.cssText = 'position:absolute;top:0;left:0;pointer-events:none;';

      wrapper.appendChild(canvas);
      wrapper.appendChild(overlay);
      inputEl.parentNode.insertBefore(wrapper, hint.nextSibling);

      var reader = new FileReader();
      reader.onload = function (e) {
        imgObj.onload = function () {
          var maxW = 400;
          var scale = imgObj.naturalWidth > maxW ? maxW / imgObj.naturalWidth : 1;
          dispW = Math.round(imgObj.naturalWidth * scale);
          dispH = Math.round(imgObj.naturalHeight * scale);

          canvas.width  = dispW;
          canvas.height = dispH;
          overlay.width  = dispW;
          overlay.height = dispH;
          canvas.style.width  = dispW + 'px';
          canvas.style.height = dispH + 'px';
          overlay.style.width  = dispW + 'px';
          overlay.style.height = dispH + 'px';
          wrapper.style.width  = dispW + 'px';

          var ctx = canvas.getContext('2d');
          ctx.drawImage(imgObj, 0, 0, dispW, dispH);
          clearOverlay();
        };
        imgObj.src = e.target.result;
      };
      reader.readAsDataURL(file);

      wrapper.addEventListener('mousedown', onMouseDown);
    });

    function onMouseDown(e) {
      var rect = canvas.getBoundingClientRect();
      state.sx = clamp(e.clientX - rect.left, 0, dispW);
      state.sy = clamp(e.clientY - rect.top,  0, dispH);
      state.dragging = true;
      clearOverlay();
      cropField.value = '';

      function onMove(ev) {
        if (!state.dragging) return;
        var rect2 = canvas.getBoundingClientRect();
        var curX = clamp(ev.clientX - rect2.left, 0, dispW);
        var curY = clamp(ev.clientY - rect2.top,  0, dispH);

        var rawW = curX - state.sx;
        var rawH = curY - state.sy;
        var sign = rawW < 0 ? -1 : 1;
        var absW = Math.abs(rawW);
        var absH = Math.abs(absW / cfg.ratio);

        state.x = sign < 0 ? Math.max(0, state.sx + rawW) : state.sx;
        state.y = state.sy;
        state.w = clamp(absW, 0, dispW - state.x);
        state.h = clamp(absH, 0, dispH - state.y);

        drawOverlay();
      }

      function onUp() {
        state.dragging = false;
        document.removeEventListener('mousemove', onMove);
        document.removeEventListener('mouseup',   onUp);

        if (state.w < 8 || state.h < 8) {
          clearOverlay();
          cropField.value = '';
          return;
        }

        var scale = imgObj.naturalWidth / dispW;
        var cx = Math.round(state.x * scale);
        var cy = Math.round(state.y * scale);
        var cw = Math.round(state.w * scale);
        var ch = Math.round(state.h * scale);
        cropField.value = JSON.stringify({ x: cx, y: cy, w: cw, h: ch });
      }

      document.addEventListener('mousemove', onMove);
      document.addEventListener('mouseup',   onUp);
    }

    function clearOverlay() {
      if (!overlay) return;
      var ctx = overlay.getContext('2d');
      ctx.clearRect(0, 0, overlay.width, overlay.height);
    }

    function drawOverlay() {
      var ctx = overlay.getContext('2d');
      ctx.clearRect(0, 0, overlay.width, overlay.height);

      ctx.fillStyle = 'rgba(0,0,0,0.45)';
      ctx.fillRect(0, 0, overlay.width, overlay.height);
      ctx.clearRect(state.x, state.y, state.w, state.h);

      ctx.strokeStyle = '#FF6B35';
      ctx.lineWidth = 2;
      ctx.strokeRect(state.x, state.y, state.w, state.h);

      var cs = 10;
      ctx.lineWidth = 3;
      [[state.x, state.y], [state.x + state.w, state.y],
       [state.x, state.y + state.h], [state.x + state.w, state.y + state.h]
      ].forEach(function(p) {
        ctx.beginPath();
        ctx.moveTo(p[0], p[1]);
        ctx.lineTo(p[0] + (p[0] === state.x ? cs : -cs), p[1]);
        ctx.moveTo(p[0], p[1]);
        ctx.lineTo(p[0], p[1] + (p[1] === state.y ? cs : -cs));
        ctx.stroke();
      });

      if (state.w > 40) {
        var scale = imgObj.naturalWidth / overlay.width;
        var lbl = Math.round(state.w * scale) + '×' + Math.round(state.h * scale) + 'px';
        ctx.font = '11px monospace';
        ctx.fillStyle = '#FF6B35';
        ctx.fillText(lbl, state.x + 4, state.y - 4 > 4 ? state.y - 4 : state.y + 14);
      }
    }
  }

  document.addEventListener('DOMContentLoaded', function () {
    Object.keys(CONFIGS).forEach(function (id) {
      var el = document.getElementById(id);
      if (el) buildCropper(el, CONFIGS[id]);
    });
  });
})();
