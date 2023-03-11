import { useState } from "react";

function sendReq() {
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
