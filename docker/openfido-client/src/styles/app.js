import styled, { css } from 'styled-components';
import {
  Layout,
  Input,
  Checkbox,
  Menu,
  Table,
  Button,
  Modal,
  Card,
  Dropdown,
} from 'antd';
import Icon from '@ant-design/icons';

import colors from 'styles/colors';

export const StyledLayout = styled(Layout)`
  height: 100vh;
  width: 100vw;
  .ant-dropdown-trigger {
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    .anticon {
      margin-left: 6px;
    }
  }
`;

export const StyledSider = styled(Layout.Sider)`
  box-shadow: 1px 0px 3px rgba(0, 0, 0, 0.1);
  z-index: 2;
`;

export const StyledContent = styled(Layout.Content)`
  height: 100vh;
  background-color: ${colors.lightBg};
  position: relative;
`;

export const StyledSection = styled.section`
  background-color: ${colors.white};
  margin: 25px 36px 25px 25px;
  header {
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid ${colors.lightGray};
    padding: 12px 25px;
  }
  > div {
    padding: 40px 25px;
  }
`;

export const StyledTitleText = css`
  font-weight: 700;
  font-size: 28px;
  line-height: 33px;
  color: ${colors.black};
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin: 0;
`;

export const StyledTitle = styled.div`
  width: 100%;
  background-color: ${colors.white};
  border-bottom: 1px solid ${colors.lightGray};
  padding: 28px 16px 20px 16px;
  padding: 1.75rem 1rem 1.25rem 1rem;
  h1 {
    ${StyledTitleText}
    margin-right: 100px;
    white-space: pre;
    overflow: hidden;
    display: flex;
    align-items: center;
    > button {
      margin-left: 16px;
      margin-left: 1rem;
    } 
  }
  > div {
    position: relative;
    display: flex;
    align-items: center;
  }
`;

export const StyledText = styled.span`
  ${({
    color, fontweight, indent, size, bordercolor, padding, margin, align, float, display,
  }) => (`
  ${color in colors ? (`
  color: ${colors[color]};
  `) : ''}
  ${fontweight ? (`
  font-weight: ${fontweight};
  `) : ''}
  ${indent ? (`
  text-indent: ${indent}px;
  `) : ''}
  ${size === 'xlarge' ? (`
  font-size: 18px;
  line-height: 21px;
  `) : ''}
  ${size === 'large' ? (`
  font-size: 16px;
  line-height: 19px;
  `) : ''}
  ${size === 'middle' ? (`
  font-size: 14px;
  font-size: 0.875rem;
  line-height: 16px;
  line-height: 1rem;
  `) : ''}
  ${size === 'small' ? (`
  font-size: 12px;
  line-height: 14px;
  `) : ''}
  ${size === 'xsmall' ? (`
  font-size: 11px;
  line-height: 12px;
  `) : ''}
  ${bordercolor ? (`
  border: 1px solid ${bordercolor in colors ? colors[bordercolor] : bordercolor};
  border-radius: 2px;
  `) : ''}
  ${padding ? (`
  padding: ${padding};
  `) : ''}
  ${margin ? (`
  margin: ${margin};
  `) : ''}
  ${align ? (`
  text-align: ${align};
  `) : ''}
  ${float ? (`
  float: ${float};
  `) : ''}
  ${display ? (`
  display: ${display};
  `) : ''}
  `)}
`;

export const StyledH2 = styled.h2`
  color: ${(props) => (props.color in colors ? colors[props.color] : (props.color || colors.darkGray))};
  font-weight: 500;
  font-size: 20px;
  line-height: 24px;
`;

export const StyledH3 = styled.h3`
  color: ${(props) => (props.color in colors ? colors[props.color] : (props.color || colors.darkGray))};
  font-size: 18px;
  line-height: 21px;
  font-weight: 500;
`;

export const StyledH4 = styled.h4`
  color: ${(props) => (props.color in colors ? colors[props.color] : (props.color || colors.gray))};
  font-weight: 500;
  font-size: 16px;
  line-height: 19px;
  margin: 0;
`;

export const StyledH5 = styled.h5`
  color: ${(props) => (props.color in colors ? colors[props.color] : (props.color || colors.gray))};
  font-size: 14px;
  line-height: 16px;
  font-weight: 500;
  margin: 0;
`;

export const StyledButton = styled(Button)`
  border: 0;
  border-radius: 3px;
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  box-shadow: none;
  .anticon {
    line-height: 0;
  }
  &.ant-btn {
    font-size: 14px;
    line-height: 16px;
    font-weight: 500;
    border-radius: 3px;
    padding: 0;
    height: auto;
    &:not(.ant-btn-text) span {
      padding: 3px 8px;
      padding: 0.1875rem 0.5rem;
    }
    label {
      cursor: pointer;
      padding: 3px 8px;
      padding: 0.1875rem 0.5rem;
    }
    &.ant-btn-sm:not(.ant-btn-text) span {
      padding: 4px 8px;
      padding: 0.25rem 0.5rem;
    }
  }
  &.ant-btn-lg { 
    font-size: 18px;
    line-height: 21px;
    padding: 8px 12px;
    padding: 0.5rem 0.75rem;
    height: 50px;
    height: 3.125rem;
  }
  &.ant-btn-sm {
    font-size: 12px;
    line-height: 14px;
    height: auto;
    font-weight: 400;
  }
  &.ant-btn[disabled], &.ant-btn[disabled]:hover, &.ant-btn[disabled]:focus {
    background-color: ${colors.lightGray};
    color: ${colors.white};
    cursor: default;
  }
  ${({
    type, color, width, height, hoverbgcolor, size, textcolor,
  }) => (`
  ${size === 'middle' ? (`
  &.ant-btn {
    font-size: 16px;
    line-height: 19px;
    font-weight: 500;
    border-radius: 3px;
    height: 50px;
    height: 3.125rem;
  }
  `) : ''}
  ${type === 'text' ? (`
  color: ${colors.blue};
  &, &.ant-btn-sm, &.ant-btn-lg {
    padding: 0;
  }
  &:hover, &:focus {
    color: ${colors.lightBlue};
    background-color: transparent;
  }
  &.ant-btn {
    height: auto;
  }
  `) : (`
  &, &:hover, &:focus {
    background-color: ${(color in colors ? colors[color] : 'transparent')};
    color: ${(color in colors ? colors.lightGrey : colors.blue)};
  }
  &:hover, &:focus {
    color: ${(color in colors ? colors.lightGrey : colors.blue)};
  }
  &.ant-btn {
    color: ${colors.white};
    ${color in colors ? (`
    background-color: ${colors[color]};
    ${hoverbgcolor in colors ? (`
    &:hover, &:focus {
      background-color: ${hoverbgcolor in colors ? colors[hoverbgcolor] : colors[color]};
    }
    `) : (`
    &:hover, &:focus {
      background-color: ${colors[color]};
    }
    `)}
    `) : (`
    background-color: ${colors.black};
    &:hover, &:focus {
      background-color: ${colors.blue};
    }
    `)}
  }
  `)}
  ${width ? (`
  width: ${width}px;
  `) : ''}
  ${height ? (`
  height: ${height}px;
  `) : ''}
  ${textcolor in colors ? (`
  color: ${colors[textcolor]};
  `) : ''}
  `)}
`;

export const StyledInput = styled(Input)`
  width: auto;
  min-width: 280px;
  padding: 12px;
  box-shadow: 10px 5px 5px black;
  border: 1px solid;
  background-color: ${colors.lightBg};
  &, &:hover:focus {
    color: ${colors.gray};
  }
  &:hover {
    &, &::placeholder {
      color: ${colors.blue};
    }
  }
  &:focus:placeholder-shown::placeholder {
    color: ${colors.lightGray};
  }
  &::selection {
    background-color: ${colors.blue};
  }
  ${({
    size, shape, bgcolor, fontWeight,
  }) => (`
  ${size === 'large' ? (`
  font-size: 18px;
  line-height: 21px;
  background-color: ${colors.overlay20};
  width: 100%;
  height: 48px;
  `) : (`
  font-size: 12px;
  line-height: 14px;
  `)}
  ${(shape === 'round' ? (`
  background-color: ${colors.white};
  font-size: 16px;
  line-height: 19px;
  height: 42px;
  height: 2.625rem;
  &:hover, &:focus {
    border: 1px solid rgba(12, 72, 107, 0.8);
  }
  &::placeholder {
    color: rgba(12, 72, 107, 0.8);
  }
  &:focus:placeholder-shown::placeholder {
    font-size: 0;
  }
  `) : (`
  ${bgcolor ? (`
  background-color: ${bgcolor};
  `) : ''}
  ${fontWeight ? (`
  font-weight: ${fontWeight};
  `) : ''}
  &::placeholder {
    color: ${colors.darkText};
  }
  &:hover, &:focus {
    box-shadow: none;
  }
  `))}
  `)}
`;

export const StyledTextArea = styled(Input.TextArea)`
box-shadow: 10px 5px 5px black;
border: 1px solid;
  &:focus {
    box-shadow: none;
  }
  color: ${colors.gray};
  &:hover {
    color: ${colors.blue};
  }
  &:hover, &:focus {
    box-shadow: none;
  }
  font-size: 18px;
  line-height: 21px;
  padding: 10px;
`;

export const StyledCheckbox = styled(Checkbox)`
  font-size: 14px;
  line-height: 16px;
  color: ${colors.gray};
  &:hover {
    color: ${colors.blue};
  }
  .ant-checkbox-inner {
    border: 1px solid ${colors.gray};
    border-radius: 3px;
  }
`;

export const StyledIcon = styled(Icon)`
  position: absolute;
  top: 0;
  right: 0;
`;

export const StyledQmark = styled(Icon)`
  position: relative;
`;

export const StyledUploadBox = styled(Icon)`
  position: relative;
`;

export const StyledMenu = styled(Menu)`
  padding: 8px 10px;
  border: 1px solid ${colors.lightGray};
  border-radius: 3px;
  box-shadow: 2px 2px 2px rgba(0, 0, 0, 0.05);
`;

export const CSSMenuItemSpan = css`
  display: inline-block;
  font-size: 12px;
  line-height: 14px;
  width: 100%;
  color: ${colors.gray};
  text-align: left;
  padding: 5px;
  height: auto;
  transition: none;
  border-radius: 3px;
  ${({ bordercolor, hoverbgcolor, hovercolor }) => (`
  &, &:hover, &:focus {
    border: 1px solid ${bordercolor in colors ? colors[bordercolor] : colors.lightBg};
  }
  &:hover, &:focus {
    background-color: ${hoverbgcolor in colors ? colors[hoverbgcolor] : colors.lightBg};
    color: ${hovercolor in colors ? colors[hovercolor] : colors.blue};
  }
  `)}
`;

export const StyledMenuItem = styled(Menu.Item)`
  padding: 0;
  background-color: transparent;
  &:hover {
    background-color: transparent;
  }
  span {
    ${CSSMenuItemSpan}
  }
  ${({ marginbottom }) => (`
  &:not(:last-child) {
    margin-bottom: ${marginbottom || 5}px;
  }
  `)}
`;

export const StyledTable = styled(Table)`
  .ant-table-thead > tr > th {
    padding: 8px;
    color: ${colors.gray40};
    font-size: 13px;
    line-height: 18px;
    background-color: transparent;
    font-weight: 400;
  }
  .ant-table-tbody > tr > td {
    padding: 12px 8px;
    color: ${colors.black};
    font-size: 14px;
    line-height: 20px;
    font-weight: 300;
    background-color: ${colors.lightBg};
    border: 0;
  }
  ${({ alternateRowColors }) => (alternateRowColors ? (`
  .ant-table-tbody > tr:nth-child(2n) > td {
    background-color: ${colors.white};
  }
  .ant-table-tbody > tr {
    &:first-child > td {
      font-weight: 500;
      background-color: ${colors.lightGrey};
    }
  }
  `) : (`
  .ant-table-tbody > tr > td {
    padding: 4px 8px;
    border-bottom: 16px solid ${colors.white};
  }
  `))}
`;

export const StyledModal = styled(Modal)`
  box-shadow: 2px 2px 3px rgba(0, 0, 0, 0.1);
  border-radius: 2px;
  &.ant-modal {
    color: ${colors.darkText};
    padding-bottom: 0;
  }
  .ant-modal-header {
    padding: 14px 36px;
    padding: 0.875rem 2.25rem;
    border-bottom: 1px solid ${colors.lightGray};
  }
  .ant-modal-title {
    ${StyledTitleText}
  }
  h3 {
    color: ${colors.darkText};
    margin-bottom: 16px;
  }
  ${({ width }) => (`
  min-width: ${width}px;
  .ant-modal-body {
    width: ${width}px;
  }
  `)}
  .ant-modal-body {
    display: flex;
    flex-direction: column;
    padding: 20px 36px 36px 36px;
    background-color: ${colors.white};
    font-size: 14px;
    line-height: 16px;
  }
  .ant-modal-content {
    box-shadow: 2px 3px 5px rgba(0, 0, 0, 0.01);
  }
`;

export const StyledModalGrid = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-gap: 58px;
  grid-row-gap: 25px;
`;

export const StyledModalCard = styled(Card)`
  text-align: center;
  height: ${({ height }) => (height > 0 ? height : 132)}px;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  border-radius: 3px;
  margin: 0 -1px;
  img {
    margin-top: 25px;
  }
  button {
    border: 0;
    width: 100%;
    height: 100%;
    border: 3px solid transparent;
    color: ${colors.darkText};
    font-size: 14px;
    line-height: 16px;
    &:hover, &:focus {
      border: 3px solid ${colors.blue};
      color: ${colors.blue}; // TODO: override antd's blue hover color in general
    }
    img {
      filter: grayscale(100%);
    }
    &:hover, &:active, &:focus {
      img {
        filter: none;
      }
    }
  }
  .ant-card-body {
    padding: 0;
    width: 100%;
    height: 100%;
  }
`;

export const StyledModalLabel = styled.div`
  font-weight: 500;
  position: absolute;
  top: 15px;
  left: 0;
  right: 100%;
  text-align: center;
  width: 100%;
`;

export const StyledDropdown = styled(Dropdown)`
  &.ant-dropdown-trigger {
    cursor: pointer;
    border-radius: 3px;
    padding: 3px 9px;
    display: inline-flex;
    align-items: center;
    margin-top: -4px;
    font-weight: 500;
    ${({ color, bordercolor }) => (`
    color: ${color in colors ? colors[color] : colors.darkText};
    border: 1px solid ${bordercolor in colors ? colors[bordercolor] : bordercolor};
    .anticon {
      margin-left: 8px;
      color: ${bordercolor in colors ? colors[bordercolor] : bordercolor};
    }
    `)}
  }
`;

export const StyledGrid = styled.div`
  display: grid;
  align-items: center;
  color: ${colors.darkText};
  ${({
    gridTemplateColumns, gridgap, padding, margin, width, bgcolor,
  }) => (`
  ${bgcolor ? (`
  background-color: ${bgcolor in colors ? colors[bgcolor] : bgcolor};
  `) : ''}
  width: ${width || '100%'};
  grid-template-columns: ${gridTemplateColumns || '1fr'};
  ${gridgap ? (`
  grid-gap: ${gridgap}px;
  `) : ''} 
  padding: ${padding || '12px 20px 12px 16px'};
  margin: ${margin || 0};
  `)}
`;
