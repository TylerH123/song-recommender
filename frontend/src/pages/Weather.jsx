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
        setSongs(res);
        setFetched(true);
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
      </main>
      {fetched && <Redirect to={{ pathname: "/songs" }} />}
    </div>
  );
};

export default Weather;
