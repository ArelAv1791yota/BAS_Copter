import cv2


class DrawingUtils:
    """Утилиты для рисования элементов на изображениях"""
    @staticmethod
    def draw_dashed_line(img, pt1, pt2, color, thickness=2, dash_length=8):
        """Рисование пунктирной линии"""
        dist = ((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2) ** 0.5
        dashes = int(dist / dash_length)
        for i in range(dashes):
            start = [int(pt1[0] + (pt2[0] - pt1[0]) * i / dashes),
                     int(pt1[1] + (pt2[1] - pt1[1]) * i / dashes)]
            end = [int(pt1[0] + (pt2[0] - pt1[0]) * (i + 0.5) / dashes),
                   int(pt1[1] + (pt2[1] - pt1[1]) * (i + 0.5) / dashes)]
            cv2.line(img, tuple(start), tuple(end), color, thickness)

    @staticmethod
    def printer_punktirnoy_linii(frame, x1, y1, x2, y2, color):
        """Рисование пунктирной прямоугольной рамки"""
        DrawingUtils.draw_dashed_line(frame, (x1, y1), (x2, y1), color, 2)
        DrawingUtils.draw_dashed_line(frame, (x2, y1), (x2, y2), color, 2)
        DrawingUtils.draw_dashed_line(frame, (x2, y2), (x1, y2), color, 2)
        DrawingUtils.draw_dashed_line(frame, (x1, y2), (x1, y1), color, 2)