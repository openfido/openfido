import styled from 'styled-components';

import colors from 'styles/colors';

export const Root = styled.div`
  width: 100%;
  height: 100vh;
  text-align: center;
  background-color: ${colors.blue};
`;

export const StyledH1 = styled.h1`
  font-size: 30px;
  font-size: 1.875rem;
  line-height: 36px;
  line-height: 2.25rem;
  font-weight: 400;
  padding-top: 100px;
  padding-top: 6.25rem;
  color: ${colors.white};
`;

export const StyledH2 = styled.h2`
  font-size: 20px;
  font-size: 1.25rem;
  line-height: 24px;
  line-height: 1.5rem;
  color: ${colors.blue};
  text-transform: uppercase;
  margin-bottom: 40px;
  margin-bottom: 2.5rem;
`;

export const StyledForm = styled.form`
  width: 390px;
  height: 522px;
  padding: 30px;
  margin: 42px auto 0 auto;
  margin: 2.625rem auto 0 auto;
  background-color: ${colors.white};
  text-align: left;
  border-radius: 3px;
`;

export const StyledInput = styled.input`
  width: 330px;
  font-size: 18px;
  font-size: 1.125rem;
  color: ${colors.gray};
  padding-bottom: 0.625rem;
  padding-left: 0.25rem;
  padding-right: 0.25rem;
  border: none;
  border-bottom: 1px solid ${colors.lightGray};
  &::placeholder {
    color: ${colors.lightGray};
  }
  &:first-of-type {
    margin-bottom: 20px;
    margin-bottom: 1.25rem;
  }
`;

export const FormMessage = styled.div`
  padding: 0.75rem 0;
  height: 2.5rem;
  margin-bottom: 20px;
  margin-bottom: 1.25rem;
`;
