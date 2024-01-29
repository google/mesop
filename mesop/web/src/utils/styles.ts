import {Style} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function formatStyle(styleObj: Style): string {
  let style = '';
  if (!styleObj) {
    return style;
  }
  if (styleObj.getAlignItems()) {
    style += `align-items: ${styleObj.getAlignItems()};`;
  }

  if (styleObj.getBackground()) {
    style += `background: ${styleObj.getBackground()};`;
  }
  if (styleObj.getBorder()) {
    const border = styleObj.getBorder()!;
    const top = border.getTop();
    if (top) {
      style += `border-top: ${top.getWidth()} ${top.getStyle()} ${top.getColor()};`;
    }
    const bottom = border.getBottom();
    if (bottom) {
      style += `border-bottom: ${bottom.getWidth()} ${bottom.getStyle()} ${bottom.getColor()};`;
    }
    const left = border.getLeft();
    if (left) {
      style += `border-left: ${left.getWidth()} ${left.getStyle()} ${left.getColor()};`;
    }
    const right = border.getRight();
    if (right) {
      style += `border-right: ${right.getWidth()} ${right.getStyle()} ${right.getColor()};`;
    }
  }
  if (styleObj.getBorderRadius()) {
    style += `border-radius: ${styleObj.getBorderRadius()};`;
  }
  if (styleObj.getBoxShadow()) {
    style += `box-shadow: ${styleObj.getBoxShadow()};`;
  }
  if (styleObj.getColor()) {
    style += `color: ${styleObj.getColor()};`;
  }
  if (styleObj.getColumns()) {
    style += `columns: ${styleObj.getColumns()};`;
  }
  if (styleObj.getDisplay()) {
    style += `display: ${styleObj.getDisplay()};`;
  }
  if (styleObj.getFlexBasis()) {
    style += `flex-basis: ${styleObj.getFlexBasis()};`;
  }
  if (styleObj.getFlexDirection()) {
    style += `flex-direction: ${styleObj.getFlexDirection()};`;
  }
  if (styleObj.getFlexGrow()) {
    style += `flex-grow: ${styleObj.getFlexGrow()};`;
  }
  if (styleObj.getFlexShrink()) {
    style += `flex-shrink: ${styleObj.getFlexShrink()};`;
  }
  if (styleObj.getFlexWrap()) {
    style += `flex-wrap: ${styleObj.getFlexWrap()};`;
  }
  if (styleObj.getFontSize()) {
    style += `font-size: ${styleObj.getFontSize()};`;
  }
  if (styleObj.getFontStyle()) {
    style += `font-style: ${styleObj.getFontStyle()};`;
  }
  if (styleObj.getFontWeight()) {
    style += `font-weight: ${styleObj.getFontWeight()};`;
  }
  if (styleObj.getGap()) {
    style += `gap: ${styleObj.getGap()};`;
  }
  if (styleObj.getHeight()) {
    style += `height: ${styleObj.getHeight()};`;
  }
  if (styleObj.getJustifyContent()) {
    style += `justify-content: ${styleObj.getJustifyContent()};`;
  }
  if (styleObj.getLetterSpacing()) {
    style += `letter-spacing: ${styleObj.getLetterSpacing()};`;
  }
  if (styleObj.getLineHeight()) {
    style += `line-height: ${styleObj.getLineHeight()};`;
  }
  if (styleObj.getMargin()) {
    const margin = styleObj.getMargin()!;
    style += `margin: ${margin.getTop() || 0} ${margin.getRight() || 0} ${
      margin.getBottom() || 0
    } ${margin.getLeft() || 0};`;
  }
  if (styleObj.getOverflowX()) {
    style += `overflow-x: ${styleObj.getOverflowX()};`;
  }
  if (styleObj.getOverflowY()) {
    style += `overflow-y: ${styleObj.getOverflowY()};`;
  }
  if (styleObj.getPadding()) {
    const padding = styleObj.getPadding()!;
    style += `padding: ${padding.getTop() || 0} ${padding.getRight() || 0} ${
      padding.getBottom() || 0
    } ${padding.getLeft() || 0};`;
  }
  if (styleObj.getPosition()) {
    style += `position: ${styleObj.getPosition()};`;
  }
  if (styleObj.getTextAlign()) {
    style += `text-align: ${styleObj.getTextAlign()};`;
  }
  if (styleObj.getTextDecoration()) {
    style += `text-decoration: ${styleObj.getTextDecoration()};`;
  }
  if (styleObj.getTextOverflow()) {
    style += `text-overflow: ${styleObj.getTextOverflow()};`;
  }
  if (styleObj.getWhiteSpace()) {
    style += `white-space: ${styleObj.getWhiteSpace()};`;
  }
  if (styleObj.getWidth()) {
    style += `width: ${styleObj.getWidth()};`;
  }
  return style;
}
