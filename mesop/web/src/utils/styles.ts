import {Style} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function formatStyle(styleObj: Style): string {
  let style = '';
  if (!styleObj) {
    return style;
  }
  if (styleObj.getBackground()) {
    style += `background: ${styleObj.getBackground()};`;
  }
  if (styleObj.getColor()) {
    style += `color: ${styleObj.getColor()};`;
  }
  if (styleObj.getFontWeight()) {
    style += `font-weight: ${styleObj.getFontWeight()};`;
  }
  if (styleObj.getFontSize()) {
    style += `font-size: ${styleObj.getFontSize()};`;
  }
  if (styleObj.getHeight()) {
    style += `height: ${styleObj.getHeight()};`;
  }
  if (styleObj.getWidth()) {
    style += `width: ${styleObj.getWidth()};`;
  }
  if (styleObj.getDisplay()) {
    style += `display: ${styleObj.getDisplay()};`;
  }
  if (styleObj.getFlexDirection()) {
    style += `flex-direction: ${styleObj.getFlexDirection()};`;
  }
  if (styleObj.getFlexGrow()) {
    style += `flex-grow: ${styleObj.getFlexGrow()};`;
  }
  if (styleObj.getAlignItems()) {
    style += `align-items: ${styleObj.getAlignItems()};`;
  }
  if (styleObj.getPosition()) {
    style += `position: ${styleObj.getPosition()};`;
  }
  if (styleObj.getTextAlign()) {
    style += `text-align: ${styleObj.getTextAlign()};`;
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
  if (styleObj.getMargin()) {
    const margin = styleObj.getMargin()!;
    style += `margin: ${margin.getTop()} ${margin.getRight()} ${margin.getBottom()} ${margin.getLeft()};`;
  }
  if (styleObj.getPadding()) {
    const padding = styleObj.getPadding()!;
    style += `padding: ${padding.getTop()} ${padding.getRight()} ${padding.getBottom()} ${padding.getLeft()};`;
  }
  return style;
}
