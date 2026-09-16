document.addEventListener("DOMContentLoaded", () => {
  const activitiesList = document.getElementById("activities-list");
  const activitySelect = document.getElementById("activity");
  const signupForm = document.getElementById("signup-form");
  const messageDiv = document.getElementById("message");
  const messageModal = document.getElementById("message-modal");
  const closeMessageButton = document.getElementById("close-message");
  const confirmMessageButton = document.getElementById("confirm-message");
  const messageIcon = document.getElementById("message-icon");

  function showMessage(message, type) {
    messageDiv.textContent = message;
    messageModal.className = `message-modal ${type}`;
    messageIcon.textContent = type === "success" ? "✓" : "!";
    messageModal.classList.remove("hidden");
    closeMessageButton.focus();
  }

  function hideMessage() {
    messageModal.classList.add("hidden");
  }

  closeMessageButton.addEventListener("click", hideMessage);
  confirmMessageButton.addEventListener("click", hideMessage);
  messageModal.addEventListener("click", (event) => {
    if (event.target === messageModal) {
      hideMessage();
    }
  });

  // Function to fetch activities from API
  async function fetchActivities() {
    try {
      const response = await fetch("/activities", { cache: "no-store" });
      const activities = await response.json();

      // Clear loading message
      activitiesList.innerHTML = "";
      activitySelect.innerHTML = '<option value="">-- Select an activity --</option>';

      // Populate activities list
      Object.entries(activities).forEach(([name, details]) => {
        const activityCard = document.createElement("div");
        const category = details.category || "general";
        activityCard.className = `activity-card category-${category}`;

        const spotsLeft = details.max_participants - details.participants.length;
        const participantBadges = details.participants.length
          ? details.participants
              .map(
                (participant) => `
                  <div class="participant-badge">
                    <span>${participant}</span>
                    <button
                      type="button"
                      class="remove-participant-btn"
                      data-activity="${name}"
                      data-email="${participant}"
                      aria-label="Remove ${participant} from ${name}"
                      title="Unregister ${participant}"
                    >
                      ×
                    </button>
                  </div>
                `
              )
              .join("")
          : '<span class="participant-empty">No participants yet</span>';

        const categoryLabel = {
          sports: "Sports",
          artistic: "Artistic",
          intellectual: "Intellectual",
          general: "General",
        }[category];

        activityCard.innerHTML = `
          <div class="activity-header">
            <h4>${name}</h4>
            <span class="activity-tag">${categoryLabel}</span>
          </div>
          <p>${details.description}</p>
          <p><strong>Schedule:</strong> ${details.schedule}</p>
          <p><strong>Availability:</strong> ${spotsLeft} spots left</p>
          <div class="participants-box">
            <strong>Participants:</strong>
            <div class="participants-list">${participantBadges}</div>
          </div>
        `;

        activitiesList.appendChild(activityCard);

        // Add option to select dropdown
        const option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        activitySelect.appendChild(option);
      });
    } catch (error) {
      activitiesList.innerHTML = "<p>Failed to load activities. Please try again later.</p>";
      console.error("Error fetching activities:", error);
    }
  }

  activitiesList.addEventListener("click", async (event) => {
    const removeButton = event.target.closest(".remove-participant-btn");
    if (!removeButton) {
      return;
    }

    const activityName = removeButton.dataset.activity;
    const email = removeButton.dataset.email;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activityName)}/unregister?email=${encodeURIComponent(email)}`,
        {
          method: "DELETE",
          cache: "no-store",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        await fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to unregister the student.", "error");
      console.error("Error unregistering student:", error);
    }
  });

  // Handle form submission
  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const activity = document.getElementById("activity").value;

    try {
      const response = await fetch(
        `/activities/${encodeURIComponent(activity)}/signup?email=${encodeURIComponent(email)}`,
        {
          method: "POST",
          cache: "no-store",
        }
      );

      const result = await response.json();

      if (response.ok) {
        showMessage(result.message, "success");
        signupForm.reset();
        await fetchActivities();
      } else {
        showMessage(result.detail || "An error occurred", "error");
      }
    } catch (error) {
      showMessage("Failed to sign up. Please try again.", "error");
      console.error("Error signing up:", error);
    }
  });

  // Initialize app
  fetchActivities();
});
