// Auto-dismiss flash messages after 5s
document.querySelectorAll('.flash').forEach(f => {
    setTimeout(() => { f.style.opacity='0'; f.style.transform='translateX(100%)'; setTimeout(()=>f.remove(),300); }, 5000);
});
