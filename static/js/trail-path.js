/*
 * Draws a winding trail path that meanders between each quest marker —
 * curving side to side like a real trail — without forming full closed
 * loops, which read as confusing "phantom circles" rather than a path.
 *
 * Works for any number of quests, and redraws itself if the window is
 * resized (since the markers reflow on smaller screens).
 */

function drawTrailPath() {
  const container = document.getElementById('trail-path');
  const svg = document.getElementById('trail-svg');
  const path = document.getElementById('trail-line');
  if (!container || !svg || !path) return;

  const markers = Array.from(container.querySelectorAll('.trail-marker-circle'));
  if (markers.length < 2) return;

  const containerRect = container.getBoundingClientRect();

  // Match the SVG's pixel size exactly to its container so marker
  // coordinates map 1:1 without needing a viewBox transform.
  svg.setAttribute('width', containerRect.width);
  svg.setAttribute('height', containerRect.height);

  const points = markers.map(marker => {
    const r = marker.getBoundingClientRect();
    return {
      x: r.left + r.width / 2 - containerRect.left,
      y: r.top + r.height / 2 - containerRect.top,
    };
  });

  path.setAttribute('d', catmullRomToBezierPath(addMeander(points)));
}

// Inserts a couple of extra waypoints between each pair of real stops and
// nudges them side to side, so the path winds gently back and forth on
// its way from stop to stop, hugging closer to the center of the trail
// rather than wandering into the text on either side.
function addMeander(points) {
  const result = [points[0]];

  for (let i = 0; i < points.length - 1; i++) {
    const p1 = points[i];
    const p2 = points[i + 1];
    const dx = p2.x - p1.x;
    const dy = p2.y - p1.y;
    const dist = Math.hypot(dx, dy);
    const dir = i % 2 === 0 ? 1 : -1;
    const wiggle = Math.min(36, dist * 0.09);

    result.push({
      x: p1.x + dx * 0.33 + dir * wiggle,
      y: p1.y + dy * 0.33,
    });
    result.push({
      x: p1.x + dx * 0.66 - dir * wiggle,
      y: p1.y + dy * 0.66,
    });
    result.push(p2);
  }

  return result;
}

// Converts a list of points into a smooth curved SVG path (a Catmull-Rom
// spline, expressed as cubic bezier segments) so the trail winds gently
// from point to point instead of bending sharply.
function catmullRomToBezierPath(points) {
  if (points.length < 2) return '';

  let d = `M ${points[0].x} ${points[0].y} `;

  for (let i = 0; i < points.length - 1; i++) {
    const p0 = points[i - 1] || points[i];
    const p1 = points[i];
    const p2 = points[i + 1];
    const p3 = points[i + 2] || p2;

    const cp1x = p1.x + (p2.x - p0.x) / 6;
    const cp1y = p1.y + (p2.y - p0.y) / 6;
    const cp2x = p2.x - (p3.x - p1.x) / 6;
    const cp2y = p2.y - (p3.y - p1.y) / 6;

    d += `C ${cp1x} ${cp1y}, ${cp2x} ${cp2y}, ${p2.x} ${p2.y} `;
  }

  return d;
}

document.addEventListener('DOMContentLoaded', drawTrailPath);

let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(drawTrailPath, 150);
});
