// Mermaid initialization for mdbook
// Converts ```mermaid code blocks to rendered diagrams
(function () {
  const darkThemes = ['ayu', 'navy', 'coal'];
  const classList = document.getElementsByTagName('html')[0].classList;

  let isDark = false;
  for (const cssClass of classList) {
    if (darkThemes.includes(cssClass)) {
      isDark = true;
      break;
    }
  }

  // Convert <code class="language-mermaid"> blocks to <pre class="mermaid">
  const codeBlocks = document.querySelectorAll('code.language-mermaid');
  codeBlocks.forEach(function (block) {
    const pre = block.parentElement;
    const div = document.createElement('pre');
    div.className = 'mermaid';
    div.textContent = block.textContent;
    pre.parentElement.replaceChild(div, pre);
  });

  if (document.querySelectorAll('.mermaid').length > 0) {
    mermaid.initialize({ startOnLoad: true, theme: isDark ? 'dark' : 'default' });
  }

  // Re-render on theme change
  for (const themeId of ['light', 'rust', 'coal', 'navy', 'ayu']) {
    const el = document.getElementById(themeId);
    if (el) {
      el.addEventListener('click', function () { window.location.reload(); });
    }
  }
})();
