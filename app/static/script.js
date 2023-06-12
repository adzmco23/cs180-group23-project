window.addEventListener("load", function () {
	// Retrieve the form elements
	var form = document.getElementById("arguments");
	var numberInputs = document.querySelectorAll('input[type="number"]');
	var dropdowns = document.querySelectorAll("select");

	// Load the last submitted values from local storage
	var storedValues = JSON.parse(localStorage.getItem("lastSubmittedValues"));

	// Set the values of number inputs and dropdowns to the stored values, if available
	if (storedValues) {
		for (var i = 0; i < numberInputs.length; i++) {
			var inputId = numberInputs[i].id;
			if (storedValues[inputId]) {
				numberInputs[i].value = storedValues[inputId];
			}
		}
		for (var j = 0; j < dropdowns.length; j++) {
			var dropdownId = dropdowns[j].id;
			if (storedValues[dropdownId]) {
				dropdowns[j].value = storedValues[dropdownId];
			}
		}
	}

	form.classList.remove('hidden');

	// Add event listener to store the values on form submission
	form.addEventListener("submit", function (event) {
		var valuesToStore = {};

		// Store the values of number inputs
		for (var i = 0; i < numberInputs.length; i++) {
			var inputId = numberInputs[i].id;
			valuesToStore[inputId] = numberInputs[i].value;
		}

		// Store the values of dropdowns
		for (var j = 0; j < dropdowns.length; j++) {
			var dropdownId = dropdowns[j].id;
			valuesToStore[dropdownId] = dropdowns[j].value;
		}

		// Store the values in local storage
		localStorage.setItem("lastSubmittedValues", JSON.stringify(valuesToStore));
	});
});
