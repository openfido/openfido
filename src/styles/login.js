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
  height: 48px;
  height: 3rem;
  color: ${colors.blue};
`;

/*const StyledH2 = styled.h2`
  font-size: 20px;
  font-size: 1.25rem;
  line-height: 24px;
  line-height: 1.5rem;
  color: ${colors.blue};
  text-transform: uppercase;
  margin-bottom: 40px;
  margin-bottom: 2.5rem;
`;*/

export const StyledForm = styled.form`
  position: relative;
  width: 390px;
  height: 522px;
  padding: 28px 32px;
  margin: 42px auto 0 auto;
  margin: 2.625rem auto 0 auto;
  background-color: ${colors.white};
  text-align: left;
  border-radius: 3px;
  label span {
    line-height: 2.5rem;
  }
  .anticon {
    top: 16px;
    top: 1rem;
    right: 16px;
    right: 1rem;
    cursor: pointer;
  }
  &.thanks {
    height: 300px;
  }
`;

export const StyledInput = styled.input`
  width: 330px;
  font-size: 18px;
  font-size: 1.125rem;
  line-height: 21px;
  line-height: 1.3125rem;
  font-weight: 400;
  color: ${colors.gray};
  padding: 10px 0;
  padding-left: 0;
  padding-right: 0;
  border: none;
  border-bottom: 1px solid ${colors.lightGray};
  border-radius: 0;
  &::placeholder {
    color: ${colors.lightGray};
  }
  margin-top: 16px;
  margin-top: 1rem;
  &:first-of-type {
    margin-top: 16px;
    margin-top: 1rem;
    margin-bottom: 16px;
    margin-bottom: 16px;
  }
`;

export const FormMessage = styled.div`
  ${({ size }) => size === 'large' ? (`
  padding: 0.75rem 0 2.25rem 0;
  height: 2.5rem;
  font-size: 14px;
  line-height: 16px;
  `) : (`
  padding-top: 0.25rem;
  font-size: 12px;
  line-height: 14px;
  height: 18px;
  height: 1.125rem;
  `)}
`;
