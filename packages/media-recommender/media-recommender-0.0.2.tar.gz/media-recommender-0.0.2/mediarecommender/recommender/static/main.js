favorites = [];

function search() {
    removeAllChild('search_results');
    var query = document.getElementById("search").value.trim();

    // Process and send the query if it does not just consist of whitespaces
    if (query) {
        var request = new XMLHttpRequest();
        request.open('GET', '/search?query=' + query);

        request.onload = function() {
            removeAllChild('search_results');
            var responseText = request.responseText;
            var search_results = JSON.parse(responseText).results;

            // For each searched title render a button within the search_result list-group
            renderListGroupButtonsFromSearchResults(search_results);
        }

        request.send();
    }
}

function submit_favorites() {
    if (favorites.length != 0) {
        // Remove all recommendation currently displayed
        removeAllChild('movie_recommendation');
        removeAllChild('game_recommendation');
        removeAllChild('book_recommendation');

        // Display a load spinner
        document.getElementById("recommendation_load_spinner").style.display = 'inline-flex';

        var favorites_json = createJSONObjectFromFavoritesArray(favorites)
        var request = new XMLHttpRequest();
        request.open('GET', '/submit?favorites=' + JSON.stringify(favorites_json));
    
        request.onload = function() {
            // Remove the load spinner
            document.getElementById("recommendation_load_spinner").style.display = 'none';

            var jsonResponse = JSON.parse(request.responseText);
            var movie_recommendation = jsonResponse.movie;
            var game_recommendation = jsonResponse.game;
            var book_recommendation = jsonResponse.book;

            renderRecommendation(movie_recommendation, 'movie_recommendation', '/static/imdb_icon.png');
            renderRecommendation(game_recommendation, 'game_recommendation', '/static/giantbomb_icon.png');
            renderRecommendation(book_recommendation, 'book_recommendation', '/static/goodreads_icon.png');
        }
    
        request.send();
    }
}

function reset() {
    removeFavorites();
    removeAllChild('movie_recommendation');
    removeAllChild('game_recommendation');
    removeAllChild('book_recommendation');
}

function renderListGroupButtonsFromSearchResults(search_results) {
    for (i = 0; i < search_results.length; i++) {
        var item_id = search_results[i].id;
        var title = search_results[i].title;
        var type = search_results[i].type;
        var button = document.createElement('button');
        button.id = item_id + '::' + title + '::' + type;
        button.classList.add('list-group-item');
        button.classList.add('list-group-item-action');
        button.textContent = title + ' (' + type + ')';  
        document.getElementById('search_results').appendChild(button);

        button.onmousedown = function() {
            // Remove the drop-down list of search results
            removeAllChild('search_results')

            // Clear the search bar
            document.getElementById('search').value = '';

            // Update the favorites array and list-group display
            if (!arrayContains(favorites, this.id)) {
                favorites.push(this.id);
                console.log(favorites);
                renderFavorites();
            }

        };
    }
}

function renderFavorites() {
    // Remove all favorites currently displayed
    removeAllChild('movie_favorites');
    removeAllChild('game_favorites');
    removeAllChild('book_favorites');

    for (i = 0; i < favorites.length; i++) {
        // Create a list item for the favorite item
        var title = favorites[i].split('::')[1];
        var type = favorites[i].split('::')[2];
        var li = document.createElement('li');
        li.id = favorites[i];
        li.classList.add('list-group-item');
        li.classList.add('clearfix');
        li.textContent = title;
        li.style.borderRadius = '10px';

        // Render the list item in the appropriate list-group depends on item type
        if (type == 'Movie') {
            document.getElementById('movie_favorites').appendChild(li);
        }
        else if (type == 'Game') {
            document.getElementById('game_favorites').appendChild(li);
        }
        else if (type == 'Book') {
            document.getElementById('book_favorites').appendChild(li);
        }

        // Create and render a delete button for the list item
        var delete_button = createDeleteButton(favorites[i]);
        li.appendChild(delete_button);
    }
}

function renderRecommendation(arr, list_group_id, icon_path) {
    for (i = 0; i < arr.length; i++) {
        var title = arr[i].title;
        var url = arr[i].url;
        var li = document.createElement('li');
        li.classList.add('list-group-item');
        li.classList.add('clearfix');
        li.id = title;
        li.textContent = title;
        li.style.borderRadius = '10px'
        document.getElementById(list_group_id).appendChild(li);

        // Create and render a url link for the list item
        var a = createItemURLLink(url, icon_path);
        li.appendChild(a);
    }
}

function createDeleteButton(id) {
    var delete_button = document.createElement('button');
    delete_button.id = id;
    delete_button.type = 'button';
    delete_button.classList.add('close');
    delete_button.innerHTML = '&times;';

    delete_button.onmousedown = function() {
        var favoriteToBeRemovedIndex = favorites.indexOf(this.id);
        favorites.splice(favoriteToBeRemovedIndex, 1);
        var liToBeRemoved = document.getElementById(this.id);
        liToBeRemoved.parentNode.removeChild(liToBeRemoved);
    };

    return delete_button;
}

function createItemURLLink(url, icon_path) {
    var a = document.createElement('a');
    a.classList.add('float-right');
    a.href = url;
    a.target = '_blank';

    // Add an icon for the url link
    var img = document.createElement('img');
    img.src = icon_path;
    a.appendChild(img);

    return a;
}

function removeFavorites() {
    favorites = [];
    removeAllChild('movie_favorites');
    removeAllChild('game_favorites');
    removeAllChild('book_favorites');
}

function removeAllChild(id) {
    var element = document.getElementById(id);
    while (element.firstChild) {
        element.removeChild(element.firstChild);
    }
}

function createJSONObjectFromFavoritesArray(arr) {
    arr_of_obj = []

    for (i = 0; i < arr.length; i++) {
        item_id = arr[i].split('::')[0];
        type = arr[i].split('::')[2];
        arr_of_obj.push({id: item_id, type: type});
    }

    return {favorites: arr_of_obj};
}

function arrayContains(arr, el) {
    return (arr.indexOf(el) > -1);
}