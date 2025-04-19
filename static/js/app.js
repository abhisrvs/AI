let currentPage = 1;

function loadTweets(page = 1) {
    $.get(`/get_tweets?page=${page}`, function(response) {
        console.log(response);
        const tweetsBody = $('#tweets-body');
        tweetsBody.empty();

        response.tweets.forEach(tweet => {
            tweetsBody.append(`<tr>
                <td>${tweet.tweet_id}</td>
                <td>${tweet.user}</td>
                <td>${tweet.text}</td>
            </tr>`);
        });

        setupPagination(response.total_pages, page, response.current,response.totalItems, response.itemsPerPage);
    });
}

function setupPagination(totalPages, current,totalItems) {
    
    const pagination = $('#pagination');
    pagination.empty();

    // Set how many page buttons you want to display around the current page
    const visibleButtons = 2;
    const halfVisible = Math.floor(visibleButtons / 2);

    // Calculate the range of pages to display
    let start = Math.max(1, current - halfVisible);
    let end = Math.min(totalPages, current + halfVisible);

    // Adjust the range if we're at the beginning or end
    if (current - halfVisible < 1) {
        end = Math.min(totalPages, end + (halfVisible - (current - 1)));
    } else if (current + halfVisible > totalPages) {
        start = Math.max(1, start - ((current + halfVisible) - totalPages));
    }

    // Add Previous button
    if (current > 1) {
        pagination.append(`<button class="page-btn page-item btn btn-outline-primary" data-page="${current - 1}">Prev</button>`);
    }

    // Add page buttons
    for (let i = start; i <= end; i++) {
        pagination.append(`<button class="page-btn page-item ${i === current ? 'active' : ''}" data-page="${i}">${i}</button>`);
    }

    // Add Next button
    if (current < totalPages) {
        pagination.append(`<button class="page-btn page-item" data-page="${current + 1}">Next</button>`);
    }

    // Handle page click
    $('.page-btn').click(function () {
        const selectedPage = $(this).data('page');
        current = selectedPage;
        loadTweets(selectedPage);
        setupPagination(totalPages, current); // Re-render pagination
    });
    
}


// $('#generate-btn').click(function () {
//     $('#loader').show();
//     $('html, body').animate({
//         scrollTop: $('#recommendations-body').offset().top
//     }, 100);
//     $.get('/generate_recommendations', function (response) {
//         $('#loader').hide();
//         const recsBody = $('#recommendations-body');
//         recsBody.empty();

//         response.recommendations.forEach(rec => {
//             recsBody.append(`<tr>
//                 <td>${rec.tweet_id}</td>
//                 <td>${rec.user}</td>
//                 <td>${rec.text}</td>
//             </tr>`);
//         });
//     });
// });

// $('#clear-btn').click(function () {
//     $.get('/clear_recommendations', function () {
//         $('#recommendations-body').empty();
//     });
// });

$(document).ready(function () {
    loadTweets();
});

function recommendTopic(event, topic) {
    event.preventDefault();

    const button = event.target;
    button.disabled = true;
    button.innerText = 'Loading...';

    const recommendationsDiv = document.getElementById('recommendations');
    if (recommendationsDiv) {
        // Show Bootstrap spinner
        recommendationsDiv.innerHTML = `
            <div class="d-flex justify-content-center align-items-center mt-4">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <strong class="ms-3">Generating recommendations for "<span style="text-transform:capitalize">${topic}</span>"... please wait</strong>
            </div>
        `;
    }

    $.get(`/recommend_topic/${encodeURIComponent(topic)}`, function(data) {
        // 5 second delay to simulate loading
        setTimeout(function () {
            button.disabled = false;
            button.innerText = 'Recommend';

            // Clear previous content
            const existingTable = document.getElementById('recommendation-table');
            if (existingTable) {
                existingTable.remove();
            }

            // Build table
            const table = document.createElement('table');
            table.id = 'recommendation-table';
            table.className = 'class="table table-bordered border-primary"';

            const thead = document.createElement('thead');
            thead.innerHTML = `
                <tr>
                    <th>#</th>
                    <th>User</th>
                    <th>Tweet</th>
                    <th>Similarity Score</th>
                </tr>
            `;
            table.appendChild(thead);

            const tbody = document.createElement('tbody');
            data.forEach((item, index) => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td>${index + 1}</td>
                    <td>@${item.user}</td>
                    <td>${item.text}</td>
                    <td>${item.score}</td>
                `;
                tbody.appendChild(tr);
            });

            table.appendChild(tbody);
            recommendationsDiv.innerHTML = `<h4 class="mt-5 mb-3 text-center">Recommendations for "${topic}"</h4>`;
            recommendationsDiv.appendChild(table);
            recommendationsDiv.scrollIntoView({ behavior: 'smooth' });
        }, 5000);
    }).fail(() => {
        button.disabled = false;
        button.innerText = 'Recommended';
        recommendationsDiv.innerHTML = `<div class="alert alert-danger mt-3">Failed to load recommendations. Please try again later.</div>`;
    });
}
