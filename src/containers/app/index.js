import React from 'react';
import PropTypes from 'prop-types';

import { StyledLayout, StyledSider, StyledContent } from 'styles/app';
import Navigation from './navigation';

const App = ({ children }) => (
  <StyledLayout>
    <StyledSider width={250} theme="light">
      <Navigation />
    </StyledSider>
    <StyledContent>
      {children}
    </StyledContent>
  </StyledLayout>
);

App.propTypes = { children: PropTypes.node.isRequired };

export default App;
