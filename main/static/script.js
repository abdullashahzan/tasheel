async function fetchUpdates() {
    try {
        const response = await fetch('/tell_crowd/');
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.json();
        console.log(data.crowd_info);
        const roadElement = document.getElementById('road');
        const densityElement = document.getElementById('density');
        if (data.crowd_info === 0) {
            roadElement.style.backgroundColor = 'green';
            densityElement.style.color = 'green';
            densityElement.innerHTML = 'Low';
        } else if (data.crowd_info === 1) {
            roadElement.style.backgroundColor = 'orange';
            densityElement.style.color = 'orange';
            densityElement.innerHTML = 'Moderate';
        } else {
            roadElement.style.backgroundColor = 'red';
            densityElement.style.color = 'red';
            densityElement.innerHTML = 'High';
        }
        // Process the data as needed
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    } finally {
        // Fetch updates again after a delay
        setTimeout(fetchUpdates, 2000); // Adjust the delay as needed
    }
}

// Start fetching updates
fetchUpdates();