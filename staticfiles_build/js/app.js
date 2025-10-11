(function() {
    [...document.querySelectorAll(".control")].forEach(button => {
        button.addEventListener("click", function() {
            document.querySelector(".active-btn").classList.remove("active-btn");
            this.classList.add("active-btn");
            document.querySelector(".active").classList.remove("active");
            document.getElementById(button.dataset.id).classList.add("active");
        })
    });
    document.querySelector(".theme-btn").addEventListener("click", () => {
        document.body.classList.toggle("light-mode");
    })
})();

function clickSubmit() {
    var name = document.getElementById("nameRec").value;
    var email = document.getElementById("emailRec").value;
    var content = document.getElementById("contentRec").value;

    const statusBox = document.getElementById("statusMessage");
    statusBox.style.display = "none"; 

    createContact(name, email, content)
        .then(() => {
            showStatus("Message sent successfully!", "#d4edda", "#28a745", "#155724");
            document.getElementById("nameRec").value = "";
            document.getElementById("emailRec").value = "";
            document.getElementById("contentRec").value = "";
            document.getElementById("subRec").value = "";
            
        })
        .catch((error) => {
            showStatus("Failed to send: " + error.message, "#f8d7da", "#dc3545", "#721c24");
        });
}

function showStatus(message, bgColor, borderColor, textColor) {
    const statusBox = document.getElementById("statusMessage");

    statusBox.innerText = message;
    statusBox.style.backgroundColor = bgColor;
    statusBox.style.borderColor = borderColor;
    statusBox.style.color = textColor;
    statusBox.style.display = "block";
    statusBox.style.opacity = "1";

    // Wait 2 seconds, then fade out
    setTimeout(() => {
        statusBox.style.opacity = "0";

        // After transition (1s), hide element
        setTimeout(() => {
            statusBox.style.display = "none";
        }, 1000);
    }, 2000);
}



function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

async function createContact(name, email, content) {
    try {
        const response = await fetch('/api/contact/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: JSON.stringify({
                name: name,
                email: email,
                content: content
            })
        });

        const data = await response.json();
        
        if (!response.ok) {
            // If we have validation errors, show them
            if (data.errors) {
                const errorMessages = Object.entries(data.errors)
                    .map(([field, errors]) => `${field}: ${errors.join(', ')}`)
                    .join('\n');
                throw new Error(errorMessages);
            }
            throw new Error(data.message || `HTTP error! status: ${response.status}`);
        }

        console.log('Success:', data);
        return data;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
