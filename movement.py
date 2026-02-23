import gpxpy
import folium

def reconstruct_movement(gpx_file_path):

    with open(gpx_file_path, 'r') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

    points = []

    for track in gpx.tracks:
        for segment in track.segments:
            for point in segment.points:
                points.append((point.latitude, point.longitude))

    if points:
        start_pos = points[0]
        m = folium.Map(location=start_pos, zoom_start=14)
        folium.PolyLine(points, color="blue", weight=2.5, opacity=1).add_to(m)
        m.save("movement_reconstruction.html")
