// Function to add event listener to the Plotly graph in #umap
function addEventListenerToUmap() {
    var umapElement = document.getElementById('umap');  // Target the #umap container

    // Check if there's a Plotly graph within #umap
    var plotElement = umapElement.querySelector('.js-plotly-plot');

    // Ensure the plot exists and check if the listener has already been added
    if (plotElement && !plotElement.hasAttribute('data-listener-added')) {
        // Attach event listener directly to Plotly plot
        plotElement.on('plotly_selected', function(eventData) {
            console.log('Plotly selected event detected:', eventData);

            
            // Custom handling of the selected points
            if (eventData) {
                // Add "loading" class to the #cluster_info element if it exists
                document.getElementById('cluster_info')?.classList.add('loading');

                const selectedIds = eventData.points.map(point => point.customdata[0]);
                console.log('Selected IDs:', selectedIds);

                // Call your custom JavaScript function here with the selected IDs
                myCustomFunction(selectedIds);
            }
        });

        plotElement.on('plotly_deselect', function() {
            console.log('Plotly deselect event detected');
            document.getElementById('cluster_info')?.classList.remove('loading');

            // Handle the deselection
            myCustomFunction([]);
        });

        plotElement.on('plotly_hover', function(data) {
            // Select the tooltip (hovertext) container
            var tooltip = document.querySelector('.hoverlayer .hovertext');

            // Set its top and left to 0 to position it at the top-left of the chart
            if (tooltip) {
                tooltip.style.transform = 'translate(200px, 0px)'
                
            }
        });

        // Add a click event listener
        plotElement.on('plotly_click', function(eventData) {
            console.log('Plotly click event detected:', eventData);

            // Custom handling of the clicked point
            if (eventData) {
                const clickedId = eventData.points[0].customdata[0];
                console.log('Clicked ID:', clickedId);

                // Call a custom function to handle the click event
                handleDotClick(clickedId);
            }
        });

        // Set an attribute to mark that the listener has been added
        plotElement.setAttribute('data-listener-added', 'true');
    }
}

// Function to handle a click on a dot
function handleDotClick(clickedId) {
    // Implement your custom logic here
    console.log('Handling click for ID:', clickedId);
    // Example: Highlight the clicked element
    const elementId = titleToIdAttr(clickedId);
    const element = document.getElementById(elementId);
    if (element) {
        element.classList.toggle('highlight');
    }
}

// Function that runs after HTMX settles new content
document.addEventListener("htmx:afterSettle", function(evt) {
    // Check if the #umap container was updated and reapply the listener
    if (document.querySelector("#umap")) {
        console.log('HTMX update detected, reapplying event listeners to #umap');
        addEventListenerToUmap();
    }
});

function titleToIdAttr(name) {
    // name to lower, replace space with -, and remove quotes and non latin characters
    return name.toLowerCase()
    .replace(/å/gi, 'a')
    .replace(/ä/gi, 'a')
    .replace(/ö/gi, 'o')
    .replace(/ /gi, '-')
    .replace(/_/gi, '-')
    .replace(/[^a-z0-9\-]/gi, '');

}

// Example custom JS function to handle selected points
function myCustomFunction(selectedIds) {
    // Do something with the selected IDs
    // Remove .hidden class from all elements with .hidden in #results
    document.querySelectorAll('#results .hidden').forEach(element => {
        element.classList.remove('hidden');
    });

    document.querySelectorAll('#results .article_item').forEach(element => {
        element.classList.add('hidden');
    });

    // Loop over selectedIds, get the titleToIdAttr, find an element with that id, add class hidden to it
    let titles = []
    selectedIds.forEach(id => {
        const elementId = titleToIdAttr(id);
        console.log(id, elementId)
        const element = document.getElementById(elementId);
        if (element) {
            element.classList.remove('hidden');
        }
        titles.push(id)
    });
    document.getElementById("selected").value = titles.join(';;;');
    const event = new CustomEvent('ihavelassoedstuff', {
        detail: { selectedIds: titles }
    });
    document.getElementById("selectedform").dispatchEvent(event);    // You can further process these IDs as needed

    // Trigger HTMX request on the form
    const form = document.getElementById("selectedform");
    if (form) {
        form.dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    }
}

// Call addEventListenerToUmap when the document is fully loaded
document.addEventListener('DOMContentLoaded', function() {
    addEventListenerToUmap();
});
