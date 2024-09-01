document.addEventListener('DOMContentLoaded', () => {
    const header = document.getElementById('header');
    const landingPage = document.querySelector('.landing_page');

    // Check if landingPage is available
    if (!landingPage) {
        console.error('Landing page element not found');
        return;
    }

    // Calculate landing page height
    const landingPageHeight = landingPage.getBoundingClientRect().height;

    // Function to update header position
    const updateHeaderPosition = () => {
        const scrollY = window.scrollY;
        
        if (scrollY >= landingPageHeight) {
            header.style.position = 'fixed';
            header.style.top = '0';
            header.style.width = '100%'; // Ensure header stays full width
        } else {
            header.style.position = 'absolute'; // Stay within the landing page
            header.style.top = `${Math.min(0, scrollY)}px`;
            header.style.width = '100%'; // Ensure header stays full width
        }
    };

    // Initial call to set header position
    updateHeaderPosition();

    // Add scroll event listener
    window.addEventListener('scroll', updateHeaderPosition);

    // Add scroll event listener
    window.addEventListener('scroll', updateHeaderPosition);

    const searchButton = document.getElementById('searchButton');

    searchButton.addEventListener('click', () => {
        // Call the function to get user location and search nearby museums
        getUserLocation();
    });
});

// Get user location
function getUserLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(sendLocationToServer, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}

function sendLocationToServer(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Send location data to your Flask server running on port 8000
    fetch('http://127.0.0.1:8000/send-location', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ latitude, longitude }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Handle the response from the server
        console.log('Nearby Museums:', data.museums);

        // Display the nearby museums on the page
        displayNearbyMuseums(data.museums);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}

// Function to display nearby museums
function displayNearbyMuseums(museums) {
    console.log('Displaying museums:', museums); // Check what data is being processed
    const museumList = document.getElementById('museum-list');
    if (!museumList) {
        console.error('Museum list element not found');
        return;
    }
    museumList.innerHTML = ''; // Clear previous content

    if (museums.length === 0) {
        museumList.innerHTML = 'No nearby museums found.';
    } else {
        museums.forEach(museum => {
            const listItem = document.createElement('li');
            listItem.textContent = museum.name;
            museumList.appendChild(listItem);
        });
    }
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}
