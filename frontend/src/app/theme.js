/**
 * Theme configuration for the application.
 * Defines the color palette used throughout the UI,
 * including backgrounds, surfaces, borders, and semantic colors.
 */

export const C = {
  // ============================================================================
  // BACKGROUND & SURFACE COLORS
  // ============================================================================
  
  /** Primary background color (dark navy) */
  bg: "#080c14",
  
  /** Primary surface/card color (slightly lighter than bg) */
  surface: "#0b1220",
  
  /** Secondary surface color for nested components */
  surface2: "#0d1626",
  
  /** Tertiary surface color for additional depth */
  surface3: "#101d30",
  
  // ============================================================================
  // BORDER COLORS
  // ============================================================================
  
  /** Primary border color for dividers and outlines */
  border: "#1a2438",
  
  /** Secondary border color for subtler boundaries */
  border2: "#1e2d47",
  
  // ============================================================================
  // TEXT COLORS
  // ============================================================================
  
  /** Primary text color (high contrast) */
  text: "#e2e8f4",
  
  /** Secondary text color for subtitles and descriptions */
  textSub: "#7a92b0",
  
  /** Muted text color for disabled or less important info */
  textMuted: "#4a6080",
  
  // ============================================================================
  // ACCENT COLORS (Primary brand color - Blue)
  // ============================================================================
  
  /** Primary accent blue */
  accent: "#3b7dd8",
  
  /** Light accent blue for highlights and interactive elements */
  accentLt: "#5b9ef4",
  
  /** Dim accent blue for backgrounds in accent areas */
  accentDim: "#0f2a50",
  
  /** Accent blue for borders and outlines */
  accentBdr: "#1e4a8a",
  
  // ============================================================================
  // SUCCESS COLORS (Green)
  // ============================================================================
  
  /** Primary green (success/positive) */
  green: "#22c55e",
  
  /** Dim green for success backgrounds */
  greenDim: "#0a2518",
  
  /** Green for success borders */
  greenBdr: "#134d2e",
  
  // ============================================================================
  // WARNING COLORS (Amber/Yellow)
  // ============================================================================
  
  /** Primary amber (warning/caution) */
  amber: "#f59e0b",
  
  /** Dim amber for warning backgrounds */
  amberDim: "#2a1a05",
  
  /** Amber for warning borders */
  amberBdr: "#5a3a0a",
  
  // ============================================================================
  // ERROR COLORS (Red)
  // ============================================================================
  
  /** Primary red (error/danger) */
  red: "#e11d48",
  
  /** Dim red for error backgrounds */
  redDim: "#2a0510",
  
  /** Red for error borders */
  redBdr: "#5a0d20",
  
  // ============================================================================
  // HIGHLIGHT COLORS (Violet & Teal)
  // ============================================================================
  
  /** Primary violet for highlights and special elements */
  violet: "#a78bfa",
  
  /** Dim violet for violet backgrounds */
  violetDim: "#1a1035",
  
  /** Violet for violet borders */
  violetBdr: "#3d2a8a",
  
  /** Primary teal for accents */
  teal: "#2dd4bf",
  
  /** Dim teal for teal backgrounds */
  tealDim: "#051a18",
  
  /** Teal for teal borders */
  tealBdr: "#0d5048"
};

// ============================================================================
// GLOBAL STYLE OBJECTS
// ============================================================================

/**
 * Global label style object.
 * Used for form labels and field descriptions.
 * Properties: small font, muted text color, uppercase weight, wide letter spacing.
 */
export const gLabel = {
  display: "block",
  fontSize: "10px",
  color: C.textMuted,
  fontWeight: 700,
  letterSpacing: ".8px",
  marginBottom: "5px"
};

/**
 * Global input style object.
 * Used for text inputs, selects, and form fields.
 * Properties: surface background, border styling, text color, border radius.
 */
export const gInput = {
  background: C.surface2,
  border: `1px solid ${C.border2}`,
  color: C.text,
  borderRadius: "7px",
  padding: "8px 11px",
  fontSize: "13px",
  width: "100%",
  outline: "none",
  boxSizing: "border-box",
  fontFamily: "inherit"
};

/**
 * Global card title style object.
 * Used for titles within card components.
 * Properties: bold text, primary color, tight letter spacing.
 */
export const gCardTitle = {
  fontSize: "13px",
  fontWeight: 700,
  color: C.text,
  margin: 0,
  letterSpacing: "-.1px"
};

/**
 * Global card header style object.
 * Used for header sections within cards.
 * Properties: padding, border separator, flexbox layout for alignment.
 */
export const gCardHeader = {
  padding: "14px 18px",
  borderBottom: `1px solid ${C.border}`,
  display: "flex",
  alignItems: "center",
  justifyContent: "space-between"
};

/**
 * Global card body style object.
 * Used for content area within cards.
 * Properties: standard padding for consistent spacing.
 */
export const gCardBody = {
  padding: "18px"
};
