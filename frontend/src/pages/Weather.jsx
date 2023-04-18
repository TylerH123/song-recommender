import { useState } from "react";
import axios from "axios";
import Songs from "./Songs";
import { Redirect } from "react-router";
const Weather = () => {
  const [zipCode, setZipCode] = useState();
  const [songs, setSongs] = useState([]);
  const [fetched, setFetched] = useState(false);
  async function sendReq(e) {
    // e.preventDefault();
    if (e.key === "Enter") {
      console.log("request");
      let url = `http://localhost:5000/recommend/${zipCode}`;
      try {
        const res = await axios.get(url, { mode: "cors" });
        // const data = res.json();
        setFetched(true);
        setSongs(res.data.songs);
        console.log(res);
      } catch (err) {
        console.log(err);
      }
    }

    // fetch(url, { credentials: "same-origin" })
    //   .then((response) => {
    //     if (!response.ok) throw Error(response.statusText);
    //     return response.json();
    //   })
    //   .then((data) => {
    //     console.log(data);
    //   })
    //   .catch((error) => console.log(error));
    // return 0;
  }
  return (

    <div className="weatherDiv">
      
      <main className="weatherMain">
        <h1>Song Recommender</h1>
        <h2>
          Input your Zipcode to get the recommended songs in the area based on
          the weather
        </h2>
        <div className="searchBox">
          <input
            type="text"
            className="searchBar"
            placeholder="Search for zipcode..."
            value={zipCode}
            onChange={(e) => setZipCode(e.target.value)}
            onKeyDown={sendReq}
          />
        </div>
        {
          // <div>
          //   {Object.keys(songs).map((genre) => (
          //     <>
          //       <h2>{genre}</h2>
          //       <ul>
          //         {songs[genre].map((song) => (
          //           <li>{song.name}</li>
          //         ))}
          //       </ul>
          //     </>
          //   ))}
          // </div>
          <>
            <link
              href="https://fonts.googleapis.com/css?family=Lato"
              rel="stylesheet"
            />
            <div className="genres-div">
              {Object.keys(songs).map((genre) => (
                <>
                  {/* <h2>{genre}</h2>
                <ul>
                  {songs[genre].map((song) => (
                    <li>{song.name}</li>
                  ))}
                </ul> */}
                  <Card genre={genre} songs={songs[genre]} />
                </>
              ))}
            </div>
          </>
        }
      </main>
    </div>
  );
};

const Card = ({ genre, songs }) => {
  return (
    <div class="card" style="width: 18rem;">
      <div class="card-header">{genre}</div>
      <ul class="list-group list-group-flush">
        {songs.map((song, index) => (
          <li class="list-group-item" key={index}>
            {song.name}
          </li>
        ))}
      </ul>
    </div>
  );
};
export default Weather;
