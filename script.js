const form = document.getElementById("leadForm");
const message = document.getElementById("formMessage");

form?.addEventListener("submit", (event) => {
  event.preventDefault();

  const data = new FormData(form);
  const company = data.get("empresa");

  message.textContent = `Obrigado, ${company}! Nossa equipe entrará em contato em breve via WhatsApp.`;
  form.reset();
});
