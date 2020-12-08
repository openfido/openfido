import styled from 'styled-components';

import colors from 'styles/colors';

export const Root = styled.div`
  width: 100%;
  min-width: 390px;
  height: 100vh;
  min-height: 768px;
  text-align: center;
  background-color: ${colors.blue};
`;

export const StyledH1 = styled.h1`
  font-size: 30px;
  font-size: 1.875rem;
  line-height: 36px;
  line-height: 2.25rem;
  font-weight: 400;
  padding-top: 69px;
  padding-top: 4.3125rem;
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

export const FormWrapper = styled.div`
  background-color: ${colors.blue};
`;

export const StyledForm = styled.form`
  position: relative;
  width: 390px;
  height: 548px;
  padding: 24px 30px;
  padding: 1.5rem 1.875rem;
  margin: 40px auto 0 auto;
  margin: 2.5rem auto 0 auto;
  background-color: ${colors.white};
  text-align: left;
  border-radius: 3px;
  > label {
    display: inline-block;
    input {
      margin-top: 0;
    }
    &:last-of-type input {
      margin-bottom: 0;
    }
    span {
      line-height: 2.25rem;
    }
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
  padding: 10px 2px;
  border: none;
  border-bottom: 1px solid ${colors.lightGray};
  border-radius: 0;
  &::placeholder {
    color: ${colors.lightGray};
  }
  margin-top: 12px;
  margin-top: 0.75rem;
  margin-bottom: 24px;
  margin-bottom: 1.5rem;
  & + div { 
    margin-top: -22px;
    margin-top: -1.375rem;
  }
  &:not(:first-of-type) {
    margin-top: 0;
  }
`;

export const FormMessage = styled.div`
  display: flex;
  justify-content: space-between;
  flex-wrap: wrap;
  ${({ size, float }) => (`
  ${size === 'large' ? (`
  padding: 0.5rem 0 1.75rem 0;
  height: 3.5rem;
  font-size: 14px;
  line-height: 16px;
  `) : (`
  padding-top: 0.25rem;
  font-size: 12px;
  line-height: 14px;
  height: 22px;
  height: 1.375rem;
  `)}
  ${float ? (`
  float: ${float};
  `) : ''}
  `)}
`;
