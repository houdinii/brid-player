// noinspection JSUnresolvedVariable
// noinspection UnnecessaryLocalVariableJS

// TODO: Change this to use a settings file
const host = "http://briandesktop:5001/";
const max_pages = 5;

function processResults(results) {
    let items = results.items;
    const results_div = document.getElementById("results");
    let html_start = `
    <table>
        <thead>
            <tr>
              <th>Details</th>
              <th>Name</th>
              <th>Size</th>
              <th>Torrent ID</th>
            </tr>
        </thead>
        <tbody>`

    let html_end = `
        </tbody>
    </table>`
    let html_middle = "";
    for (let i = 0; i < items.length; i++) {
        const result = items[i];
        // const result_div = document.createElement("div");

        let row_html = `
            <tr>
              <td><button id=${result.torrentId} class='btnDetails' type='submit'>Details</button></td>
              <td>${result.name}</td>
              <td>${result.size}</td>
              <td>${result.torrentId}</td>
            </tr>`
        html_middle += row_html;
    }
    results_div.innerHTML = html_start + html_middle + html_end;
    // results_div.append(html_end);

    function processDetails(data, torrentId) {
        const details_div = document.getElementById("details");
        const gallery_div = document.getElementById("gallery");

        let html_string = "<br/><br/><hr/><br/>";
        let check_link_btn_html = `<button id='check${torrentId}' class='btnCheckLink' type='submit'>Check Link</button>`;
        let dl_btn_html = `<button id='${torrentId}' class='btnDownload' type='submit'>Download</button>`;
        let thumbnail_html = "";
        let name_html = "";
        let description_html = "";
        let language_html = "";
        let genre_html = "";
        let size_html = "";
        let type_html = "";
        let uploadDate_html = "";
        let seeders_html = "";
        let leechers_html = "";

        if (data.thumbnail != null) {thumbnail_html
            += `<img src="${data.thumbnail}" alt="${data.shortName} Thumbnail" onerror='this.style.display = "none"'><br/><br/>`;}
        if (data.name != null) {name_html
            += `<h3>${data.name}</h3>`;}
        if (data.description != null) {description_html
            += `<em>Description:</em> ${data.description}<br/>`;}
        if (data.language != null) {language_html
            += `<em>Language:</em> ${data.language}<br/>`;}
        if (data.genre != null) {genre_html
            += `<em>Genre:</em> ${data.genre}<br/>`;}
        if (data.size != null) {size_html
            += `<em>Size:</em> ${data.size}<br/>`;}
        if (data.type != null) {type_html
            += `<em>Type:</em> ${data.type}<br/>`;}
        if (data.uploadDate != null) {uploadDate_html
            += `<em>Upload Date:</em> ${data.uploadDate}<br/>`;}
        if (data.seeders != null) {seeders_html
            += `<em>Seeders:</em> ${data.seeders}<br/>`;}
        if (data.leechers != null) {leechers_html
            += `<em>Leechers:</em> ${data.leechers}<br/>`;}

        html_string += thumbnail_html
            + name_html
            + "<p>"
            + description_html
            + language_html
            + genre_html
            + size_html
            + type_html
            + uploadDate_html
            + seeders_html
            + leechers_html
            + check_link_btn_html
            + dl_btn_html
            + "</p>";

        let img_html_string = "";
        if (data.images.length > 0) {
            img_html_string += `<p><em>Images:</em></p>`;

            for (let i = 0; i < data.images.length; i++) {
                img_html_string += `<br><img src="${data.images[i]}" alt="${data.shortName} Screenshot #${i+1}" onerror='this.style.display = "none"'/>`;
            }
        }

        // html_string += img_html_string;
        gallery_div.innerHTML = img_html_string;
        details_div.innerHTML = html_string;

        $(".btnDownload").click(function(){
            const torrentId = $(this).attr("id");
            console.log(torrentId);

            fetch(host + 'add/' + torrentId)
                // .then(response => response.json())
                .then(data => {
                    console.log(data);
                    alert("Torrent downloaded to Real Debrid")
                })
                .catch(error => {
                    console.log(error);
                    alert("Error downloading torrent to Real Debrid");
                })
            });
        $(".btnCheckLink").click(function(){
            const torrentId = $(this).attr("id").substring(5);
            // alert(`Check link button clicked for torrent with id: ${torrentId}`);

            // Get magnet link from torrentId
            // check url based on magnet link
            fetch(host + 'CheckMagnetFromId/' + torrentId)
                .then(response => response.json())
                .then(result => {
                    console.log(`RESULT: ${result}`);
                    if (result) {
                        // alert("Magnet link is available!");
                        $('.btnDownload').addClass('found');
                    } else {
                        // alert("Magnet link is not available!");
                        $('.btnDownload').addClass('not-found');
                    }
                })
                .catch(error => {
                    console.log(error);
                    alert("Error checking magnet link");
                });
        })
    }

    $(".btnDetails").click(function(){
        const torrentId = $(this).attr("id");
        console.log(torrentId);
        fetch(host + 'details/' + torrentId)
            .then(response => response.json())
            .then(data => {
                // console.log(data);
                 $('html,body').animate({
                    scrollTop: $("#details").offset().top}, 'slow');
                processDetails(data, torrentId);
            })
            .catch(error => {
                console.log(error);
                alert("Error getting torrent details!");
            })
    })
    }

function submit_search() {
    const search_string = document.getElementById("txtQuery").value;
    if (search_string === "") {
        alert("Please enter a search string.");
        return false;
    }

    // convert to url encoded string
    // let querystr = search_string + " 1080p"
    let querystr = search_string
    const search_string_encoded = encodeURIComponent(querystr);

    fetch(host + 'get/' + search_string_encoded)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            processResults(data);
        })
    return true;
}

function popular(movies=true, week=false){
    let fetch_string = host;
    if(movies === true){
        if(week === true){
            fetch_string += "PopularMovieWeek/";
        }
        else{
            fetch_string += "PopularMovie/";
        }
    } else {
        if(week === true){
            fetch_string += "PopularTVWeek/";
        }
        else{
            fetch_string += "PopularTV/";
        }
    }

    fetch(fetch_string)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            processResults(data);
        })
    return true;
}

function trending(movies=true, week=false){
    let fetch_string = host;
    if(movies === true){
        if(week === true){
            fetch_string += "TrendingMovieWeek/";
        }
        else{
            fetch_string += "TrendingMovie/";
        }
    } else {
        if(week === true){
            fetch_string += "TrendingTVWeek/";
        }
        else{
            fetch_string += "TrendingTV/";
        }
    }

    fetch(fetch_string)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            processResults(data);
        })
    return true;
}

function top100(movies=true){
    let fetch_string = host;
    if(movies === true){
        fetch_string += "Top100Movie/";
    } else {
        fetch_string += "Top100TV/";
    }

    fetch(fetch_string)
        .then(response => response.json())
        .then(data => {
            console.log(data);
            processResults(data);
        })
    return true;
}

$(document).ready(function(){
    $("#btnSearch").click(function(){
        console.log("Searching...")
        submit_search();
    });
    $("#btnPopularMoviesWeek").click(function(){
        console.log(`btnPopularMoviesWeek Clicked.`);
        popular(true, true);
    })
    $("#btnPopularMovies").click(function(){
        console.log(`btnPopularMovies Clicked.`);
        popular(true, false);
    })
    $("#btnPopularTVWeek").click(function(){
        console.log(`btnPopularTVWeek Clicked.`);
        popular(false, true);
    })
    $("#btnPopularTV").click(function(){
        console.log(`btnPopularTV Clicked.`);
        popular(false, false);
    })
    $("#btnTrendingMoviesWeek").click(function(){
        console.log(`btnTrendingMoviesWeek Clicked.`);
        trending(true, true);
    })
    $("#btnTrendingMovies").click(function(){
        console.log(`btnTrendingMovies Clicked.`);
        trending(true, false);
    })
    $("#btnTrendingTVWeek").click(function(){
        console.log(`btnTrendingTVWeek Clicked.`);
        trending(false, true);
    })
    $("#btnTrendingTV").click(function(){
        console.log(`btnTrendingTV Clicked.`);
        trending(false, false);
    })
    $("#btnTop100Movies").click(function(){
        console.log(`btnTop100Movies Clicked.`);
        top100(true);
    })
    $("#btnTop100TV").click(function(){
        console.log(`btnTop100TV Clicked.`);
        top100(false);
    })
});