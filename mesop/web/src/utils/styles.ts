import {Style} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

export function formatStyle(styleObj: Style): string {
  let style = '';
  if (!styleObj) {
    return style;
  }
  if (styleObj.getAlignContent()) {
    style += `align-content: ${styleObj.getAlignContent()};`;
  }
  if (styleObj.getAlignItems()) {
    style += `align-items: ${styleObj.getAlignItems()};`;
  }
  if (styleObj.getAlignSelf()) {
    style += `align-self: ${styleObj.getAlignSelf()};`;
  }
  if (styleObj.getAspectRatio()) {
    style += `aspect-ratio: ${styleObj.getAspectRatio()};`;
  }
  if (styleObj.getBackdropFilter()) {
    style += `backdrop-filter: ${styleObj.getBackdropFilter()};`;
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
  if (styleObj.getBottom()) {
    style += `bottom: ${styleObj.getBottom()};`;
  }
  if (styleObj.getBoxShadow()) {
    style += `box-shadow: ${styleObj.getBoxShadow()};`;
  }
  if (styleObj.getBoxSizing()) {
    style += `box-sizing: ${styleObj.getBoxSizing()};`;
  }
  if (styleObj.getColor()) {
    style += `color: ${styleObj.getColor()};`;
  }
  if (styleObj.getColumnGap()) {
    style += `column-gap: ${styleObj.getColumnGap()};`;
  }
  if (styleObj.getColumns()) {
    style += `columns: ${styleObj.getColumns()};`;
  }
  if (styleObj.getCursor()) {
    style += `cursor: ${styleObj.getCursor()};`;
  }
  if (styleObj.getDisplay()) {
    style += `display: ${styleObj.getDisplay()};`;
  }
  if (styleObj.getFlex()) {
    style += `flex: ${styleObj.getFlex()};`;
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
  if (styleObj.getFontFamily()) {
    style += `font-family: ${styleObj.getFontFamily()};`;
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
  if (styleObj.getGridArea()) {
    style += `grid-area: ${styleObj.getGridArea()};`;
  }
  if (styleObj.getGridAutoColumns()) {
    style += `grid-auto-columns: ${styleObj.getGridAutoColumns()};`;
  }
  if (styleObj.getGridAutoFlow()) {
    style += `grid-auto-flow: ${styleObj.getGridAutoFlow()};`;
  }
  if (styleObj.getGridAutoRows()) {
    style += `grid-auto-rows: ${styleObj.getGridAutoRows()};`;
  }
  if (styleObj.getGridColumn()) {
    style += `grid-column: ${styleObj.getGridColumn()};`;
  }
  if (styleObj.getGridColumnStart()) {
    style += `grid-column-start: ${styleObj.getGridColumnStart()};`;
  }
  if (styleObj.getGridColumnEnd()) {
    style += `grid-column-end: ${styleObj.getGridColumnEnd()};`;
  }
  if (styleObj.getGridRow()) {
    style += `grid-row: ${styleObj.getGridRow()};`;
  }
  if (styleObj.getGridRowStart()) {
    style += `grid-row-start: ${styleObj.getGridRowStart()};`;
  }
  if (styleObj.getGridRowEnd()) {
    style += `grid-row-end: ${styleObj.getGridRowEnd()};`;
  }
  if (styleObj.getGridTemplateAreasList()) {
    style += `grid-template-areas: ${styleObj
      .getGridTemplateAreasList()
      .map((a) => `"${a}"`)
      .join(' ')};`;
  }
  if (styleObj.getGridTemplateColumns()) {
    style += `grid-template-columns: ${styleObj.getGridTemplateColumns()};`;
  }
  if (styleObj.getGridTemplateRows()) {
    style += `grid-template-rows: ${styleObj.getGridTemplateRows()};`;
  }
  if (styleObj.getHeight()) {
    style += `height: ${styleObj.getHeight()};`;
  }
  if (styleObj.getJustifyContent()) {
    style += `justify-content: ${styleObj.getJustifyContent()};`;
  }
  if (styleObj.getJustifyItems()) {
    style += `justify-items: ${styleObj.getJustifyItems()};`;
  }
  if (styleObj.getJustifySelf()) {
    style += `justify-self: ${styleObj.getJustifySelf()};`;
  }
  if (styleObj.getLeft()) {
    style += `left: ${styleObj.getLeft()};`;
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
  if (styleObj.getMaxHeight()) {
    style += `max-height: ${styleObj.getMaxHeight()};`;
  }
  if (styleObj.getMaxWidth()) {
    style += `max-width: ${styleObj.getMaxWidth()};`;
  }
  if (styleObj.getMinHeight()) {
    style += `min-height: ${styleObj.getMinHeight()};`;
  }
  if (styleObj.getMinWidth()) {
    style += `min-width: ${styleObj.getMinWidth()};`;
  }
  if (styleObj.getObjectFit()) {
    style += `object-fit: ${styleObj.getObjectFit()};`;
  }
  if (styleObj.getOpacity()) {
    style += `opacity: ${styleObj.getOpacity()};`;
  }
  if (styleObj.getOutline()) {
    style += `outline: ${styleObj.getOutline()};`;
  }
  if (styleObj.getOverflowWrap()) {
    style += `overflow-wrap: ${styleObj.getOverflowWrap()};`;
  }
  if (styleObj.getOverflow()) {
    style += `overflow: ${styleObj.getOverflow()};`;
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
  if (styleObj.getPlaceItems()) {
    style += `place-items: ${styleObj.getPlaceItems()};`;
  }
  if (styleObj.getPointerEvents()) {
    style += `pointer-events: ${styleObj.getPointerEvents()};`;
  }
  if (styleObj.getPosition()) {
    style += `position: ${styleObj.getPosition()};`;
  }
  if (styleObj.getRight()) {
    style += `right: ${styleObj.getRight()};`;
  }
  if (styleObj.getRotate()) {
    style += `rotate: ${styleObj.getRotate()};`;
  }
  if (styleObj.getRowGap()) {
    style += `row-gap: ${styleObj.getRowGap()};`;
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
  if (styleObj.getTextShadow()) {
    style += `text-shadow: ${styleObj.getTextShadow()};`;
  }
  if (styleObj.getTextTransform()) {
    style += `text-transform: ${styleObj.getTextTransform()};`;
  }
  if (styleObj.getTop()) {
    style += `top: ${styleObj.getTop()};`;
  }
  if (styleObj.getTransform()) {
    style += `transform: ${styleObj.getTransform()};`;
  }
  if (styleObj.getTransition()) {
    style += `transition: ${styleObj.getTransition()};`;
  }
  if (styleObj.getVerticalAlign()) {
    style += `vertical-align: ${styleObj.getVerticalAlign()};`;
  }
  if (styleObj.getVisibility()) {
    style += `visibility: ${styleObj.getVisibility()};`;
  }
  if (styleObj.getWhiteSpace()) {
    style += `white-space: ${styleObj.getWhiteSpace()};`;
  }
  if (styleObj.getWidth()) {
    style += `width: ${styleObj.getWidth()};`;
  }
  if (styleObj.getWordWrap()) {
    style += `word-wrap: ${styleObj.getWordWrap()};`;
  }
  if (styleObj.getZIndex()) {
    style += `z-index: ${styleObj.getZIndex()};`;
  }
  return style;
}
