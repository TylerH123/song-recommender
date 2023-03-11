import { useState } from "react";

function sendReq() {
  let url = "http://localhost:5000/songs/"
  fetch(url, { credentials: "same-origin" })
    .then((response) => {
      if (!response.ok) throw Error(response.statusText);
      return response.json();
    })
    .then((data) => {
      console.log(data);
    })
    .catch((error) => console.log(error));
  return 0;
}

const Weather = () => {
  const [zipCode, setZipCode] = useState();
  return (
    <div className="weatherDiv">
      <main className="weatherMain">
        <div className="searchBox">
          <form onSubmit={this.sendReq}>
            <input
              type="text"
              className="searchBar"
              placeholder="Search for zipcode..."
              value={zipCode}
            />
          </form>
        </div>
      </main>
    </div>
  );
};

export default Weather;
