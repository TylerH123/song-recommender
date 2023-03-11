import { useState } from "react";
import axios from "axios";
const Weather = () => {
  const [zipCode, setZipCode] = useState();
  async function sendReq() {
    console.log("request");
    let url = `http://localhost:5000/recommend/${zipCode}`;
    try {
      const res = await axios.get(url);
      const data = res.json();
      console.log(data);
    } catch (err) {
      console.log(err);
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
          <form onSubmit={sendReq}>
            <input
              type="text"
              className="searchBar"
              placeholder="Search for zipcode..."
              value={zipCode}
              onChange={(e) => setZipCode(e.target.value)}
            />
          </form>
        </div>
      </main>
    </div>
  );
};

export default Weather;
