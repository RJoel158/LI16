(function () {
  const clock = document.createElement('div');
  clock.id = 'li16-system-clock';
  clock.style.cssText = 'position:fixed;right:12px;bottom:12px;z-index:9999;background:white;border:1px solid #777;padding:8px 12px;color:#111;font:14px Arial';
  document.body.appendChild(clock);
  function tick() {
    clock.textContent = 'Hora del sistema: ' + new Date().toLocaleString('es-BO', {timeZone:'America/La_Paz',hour12:false}) + ' (UTC-4)';
  }
  tick(); setInterval(tick, 1000);
})();
