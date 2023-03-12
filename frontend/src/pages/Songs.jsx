import React from "react";

const Songs = ({ songs }) => {
  return <div>{songs.map((song) => song.map((s) => s.name))}</div>;
};

export default Songs;
