import React from 'react'
import Signup from './Signup'
import ShowProfile from './ShowProfile'
import Login from './Login'
import { Container } from 'react-bootstrap'
import { AuthProvider } from '../contexts/AuthContext'
import {BrowserRouter, Switch, Route} from "react-router-dom"
import PrivateRoute from './PrivateRoute'
import ForgotPassword from './ForgotPassword'
import UpdateProfile from './UpdateProfile'
import Landing from './Landing'
import Hero from './Hero'
import Uploadn from './Uploadn'
import Uploadp from './Uploadp'
import Uploads from './Uploads'
import Anythingmore from './Anythingmore'
import Wait from './Wait'
import Dashboard from './Dashboard'
import Sortedpyq from './Sortedpyq'
import Generalpyq from './Generalpyq'
import Repetitivepyq from './Repetitivepyq'
import StudyPlanner from './Studyplanner'
import Uploadn1 from './Uploadn1'
import Uploadp1 from './Uploadp1'
import Uploads1 from './Uploads1'
import Topiclist from './Topiclist'
import Quiz from './Quiz'
import Learnnote from './Learnnote'
import Days from './Days'


const App = () => {
  return (
   
    <Container className="d-flex align-items-center justify-content-center" style={{ minHeight: "100vh"}}>
       
      <div className="w-100" style={{ maxWidth: "400px"}}>
      <AuthProvider>
        <BrowserRouter>
        <Switch>
            <PrivateRoute exact path="/" component={Landing} />
            <Route path="/signup" component={Signup} />
            <Route path="/login" component={Login} />
            <Route path="/forgot-password" component={ForgotPassword} />
            <PrivateRoute path="/show-profile" component={ShowProfile} />
            <PrivateRoute path="/update-profile" component={UpdateProfile} />
            <Route path="/hero" component={Hero} />
            <Route path="/uploadn" component={Uploadn} />
            <Route path="/uploadp" component={Uploadp} />
            <Route path="/uploads" component={Uploads} />
            <Route path="/anythingmore" component={Anythingmore} />
            <Route path="/wait" component={Wait} />
            <Route path="/dashboard" component={Dashboard} />
            <Route path="/sortedpyq" component={Sortedpyq} />
            <Route path="/generalpyq" component={Generalpyq} />
            <Route path="/repetitivepyq" component={Repetitivepyq} />
            <Route path="/studyplanner" component={StudyPlanner} />
            <Route path="/uploadn1" component={Uploadn1} />
            <Route path="/uploadp1" component={Uploadp1} />
            <Route path="/uploads1" component={Uploads1} />
            <Route path="/topiclist" component={Topiclist} />
            <Route path="/quiz" component={Quiz} />
            <Route path="/learnnote" component={Learnnote} />
            <Route path="/days" component={Days} />
            
          </Switch>
        </BrowserRouter>
      </AuthProvider>
      </div>
    </Container>
   
  )
}

export default App