document.addEventListener("DOMContentLoaded", function() {
  const departments = {
    Nairobi: [
      "Chemical Engineering and Allied Processes Research (CEAP-RC)",
      "Energy Resources and Energy Efficiency Research (EREE-RC)",
      "Engineering and ICT Research (EICT-RC)",
      "Environmental Sustainability and Climate Change Research (ESCC-RC)",
      "Food Technology Research (FT-RC)",
      "Industrial Materials Research (IM-RC)",
      "Industrial Microbiology and Biotechnology Research (IMB-RC)",
      "Industrial Linkages, Policy and IP Research (ILPIP-RC)",
      "Central Analytical Services (CAS)"
    ],
    Kisumu: [
      "Chemical Engineering and Allied Processes Research (CEAP-RC)",
      "Energy Resources and Energy Efficiency Research (EREE-RC)",
      "Engineering and ICT Research (EICT-RC)",
      "Environmental Sustainability and Climate Change Research (ESCC-RC)",
      "Food Technology Research (FT-RC)",
      "Industrial Materials Research (IM-RC)",
      "Industrial Microbiology and Biotechnology Research (IMB-RC)",
      "Industrial Linkages, Policy and IP Research (ILPIP-RC)",
      "Central Analytical Services (CAS)"
    ],
    Migori: ["Migori"],
    Garissa: ["Garissa"],
    Uasin_Gishu: ["Uasin Gishu"],
    Malindi: ["Malindi"],
    Kisii: ["Kisii"],
    Bungoma: ["Bungoma"]
  };

  const centerSelect = document.getElementById("center");
  const departmentSelect = document.getElementById("department");

  if (!centerSelect || !departmentSelect) return; // defensive check

  centerSelect.addEventListener("change", function() {
    const selectedCenter = this.value;
    departmentSelect.innerHTML = '<option value="">Select Department</option>';

    if (departments[selectedCenter]) {
      departments[selectedCenter].forEach(dep => {
        const option = document.createElement("option");
        option.value = dep.toLowerCase().replace(/\s+/g, "_");
        option.textContent = dep;
        departmentSelect.appendChild(option);
      });
    }
  });
});

// if (!document.getElementById('consentCheck').checked) {
//     e.preventDefault();
//     showMessage('Please check the consent box before submitting your application.', 'error');
//     return;
// }