import Topbar from "./components/topbar/Topbar";
import Sidebar from "./components/sidebar/Sidebar";
import Home from "./pages/home/home";
import helloworld from "./pages/helloworld/helloworld"
import CreateClients from "./pages/create_clients/CreateClients"
/* import {CreateClients} from "./pages/create_clients/CreateClients";
import ManageClients from "./pages/manage_clients/ManageClients";
import ClientOptions from "./pages/client_options/ClientOptions" */
import {ViewClients} from "./pages/view_clients/ViewClients";
import {ViewSites} from "./pages/view_sites/ViewSites";
//import Error404 from "./pages/error_pages/Error404";
import "./App.css";
import { BrowserRouter as Router, Route, Switch} from "react-router-dom";
import React, {useState} from "react";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min';
import ScrollToTop from "./components/scrolltotop/ScrollToTop";

function App() {

  const [showSidebarAndTopbar, setShowSidebarAndTopbar] = useState(true);
  const handleToggleSidebar = () => {
      setShowSidebarAndTopbar(!showSidebarAndTopbar);
  } 

    return (
        <Router>
            <ScrollToTop>
                {showSidebarAndTopbar && <Topbar />}
                <div className="main">
                    {showSidebarAndTopbar && <Sidebar />}
                    <Switch>
                        <Route exact path="/" component={Home} />
    {/*                     <Route path="/client_options" component={ClientOptions} />
                        <Route path="/create_clients" component={CreateClients} /> */}
                        <Route path="/view_clients" component={ViewClients} />
                        <Route path="/hello_world" component={helloworld} />
                        <Route path="/view_sites" component={ViewSites} />
                        <Route path="/create_clients" component={CreateClients}/>
    {/*                     <Route path="/manage_clients" component={ManageClients} /> */}
                    </Switch>
                </div>
            </ScrollToTop>
        </Router>
    );
}

export default App;