// Insert a symbol into the specified textarea
function insertSymbol(symbol, targetId) {
    const textarea = document.getElementById(targetId);
    const cursorPosition = textarea.selectionStart;
    const textBefore = textarea.value.substring(0, cursorPosition);
    const textAfter = textarea.value.substring(cursorPosition);
    textarea.value = textBefore + symbol + textAfter;
    textarea.focus();
    textarea.setSelectionRange(cursorPosition + symbol.length, cursorPosition + symbol.length);
}

// Update MathJax preview (if needed later)
document.querySelectorAll('textarea').forEach(textarea => {
    textarea.addEventListener('input', () => {
        const preview = document.getElementById('math-preview');
        if (preview) {
            preview.innerHTML = `\\[${textarea.value}\\]`;
            MathJax.typesetPromise([preview]);
        }
    });
});
