let currentTerms = [];
let generated = false;

const form = document.getElementById("generatorForm");
const typeSelect = document.getElementById("document_type");
const preview = document.getElementById("preview");
const statusBox = document.getElementById("status");
const notice = document.getElementById("notice");
const generateBtn = document.getElementById("generateBtn");

function toggleFields() {
  const type = typeSelect.value;
  document.getElementById("employmentFields").classList.toggle("hidden", type !== "employment");
  document.getElementById("ndaFields").classList.toggle("hidden", type !== "nda");
  document.getElementById("leaseFields").classList.toggle("hidden", type !== "lease");
}
typeSelect.addEventListener("change", toggleFields);
toggleFields();

function renderTerms(terms) {
  const body = document.querySelector("#termsTable tbody");
  body.innerHTML = "";
  for (const item of terms) {
    const row = document.createElement("tr");
    const a = document.createElement("td");
    const b = document.createElement("td");
    a.textContent = item.term || "";
    b.textContent = item.value || "";
    row.append(a,b);
    body.appendChild(row);
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  generateBtn.disabled = true;
  statusBox.textContent = "Generating draft...";
  generated = false;

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      body: new FormData(form)
    });
    const data = await response.json();

    if (!response.ok || data.error) {
      throw new Error(data.error || "Generation failed.");
    }

    preview.value = data.content || "";
    currentTerms = data.terms || [];
    renderTerms(currentTerms);
    generated = true;
    notice.textContent = data.notice || "Draft generated.";
    statusBox.textContent = "Draft generated successfully.";
  } catch (error) {
    statusBox.textContent = error.message;
  } finally {
    generateBtn.disabled = false;
  }
});

async function exportDoc(fmt) {
  if (!generated || !preview.value.trim()) {
    alert("Generate a document first.");
    return;
  }

  const data = new FormData();
  data.append("content", preview.value);
  data.append("terms_json", JSON.stringify(currentTerms));
  data.append("company_name", document.querySelector('[name="company_name"]').value);
  data.append("fmt", fmt);
  data.append("filename_stem", "LegalEase_" + fmt);

  const response = await fetch("/api/export", {method:"POST", body:data});
  if (!response.ok) {
    alert("Export failed.");
    return;
  }

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `LegalEase_Document.${fmt}`;
  a.click();
  URL.revokeObjectURL(url);
}
