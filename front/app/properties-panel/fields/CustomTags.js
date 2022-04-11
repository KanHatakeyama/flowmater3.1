import React from 'react';
import ReactTagInput from "@pathofdev/react-tag-input";
import "@pathofdev/react-tag-input/build/index.css";

import { updateGraph } from "./../../graphs/routing"
import { currentGraph } from '..';

// custom tag box
export function CustomTags() {
  const [tags, setTags] = React.useState(currentGraph.tags)
  // const [tags, setTags] = React.useState(["aa","bb"])
  return (
    <>
      <ReactTagInput
        tags={tags}
        onChange={(newTags) => {
          setTags(newTags)
          currentGraph.tags = newTags
          //convert to string style (split with comma)
          updateGraph(currentGraph.pk, { "tags": currentGraph.tags.join(",") })
        }}
      />
    </>
  )
}


