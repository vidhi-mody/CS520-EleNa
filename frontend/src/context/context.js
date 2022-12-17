import { createContext, useContext,useState } from 'react';
import { useRef } from "react";
const RoutingContext = createContext();
function RoutingContextProvider({children}) {
  const markers = useRef([]);
  const routing_info = useState({
    geoJson: null,
    markers: markers
  });
  return <RoutingContext.Provider value={routing_info}>{children}</RoutingContext.Provider>;
};
function useRoutingContext() {
  return useContext(RoutingContext);
}

export {RoutingContextProvider, useRoutingContext}