import abc
from pathlib import Path
from typing import TypeVar

from PIL import Image

_SIZE = TypeVar("_SIZE", int, tuple[int, int])


class FillAlgorithm(abc.ABC):
    @abc.abstractmethod
    def make_background(self, img_file: Path, desktop_size: _SIZE) -> Image:
        pass


class TiledStrategy(FillAlgorithm):
    """타일 형태로 이미지를 배치하는 전략"""

    def make_background(self, img_file: Path, desktop_size: _SIZE) -> Image:
        """
        출력의 높이와 너비를 입력 이미지의 높이와 너비로 나눔.
        num_tiles 시퀀스는 너비와 높이에 대해 동일한 계산을 수행.
        너비와 높이가 동일한 방식으로 처리되도록 하기 위해 리스트 컴프리헨션을 통해 계산된 2-튜플.
        """

        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        num_tiles = [o // i + 1 for o, i in zip(out_img.size, in_img.size)]

        for x in range(num_tiles[0]):
            for y in range(num_tiles[1]):
                out_img.paste(
                    in_img,
                    (
                        in_img.size[0] * x,
                        in_img.size[1] * y,
                        in_img.size[0] * (x + 1),
                        in_img.size[1] * (y + 1),
                    ),
                )

        return out_img


class CenteredStrategy(FillAlgorithm):
    """크기를 조정하지 않고 이미지를 중앙에 배치하는 채우기 전략"""

    def make_background(self, img_file: Path, desktop_size: _SIZE) -> Image:
        in_img = Image.open(img_file)
        out_img = Image.new("RGB", desktop_size)
        left = (out_img.size[0] - in_img.size[0]) // 2
        top = (out_img.size[1] - in_img.size[1]) // 2
        out_img.paste(in_img, (left, top, left + in_img.size[0], top + in_img.size[1]))

        return out_img


class ScaledStrategy(FillAlgorithm):
    """전체 화면을 채우도록 이미지를 확대하는 채우기 알고리즘"""

    def make_background(self, img_file: Path, desktop_size: _SIZE) -> Image:
        in_img = Image.open(img_file)
        out_img = in_img.resize(desktop_size)

        return out_img


class Resizer:
    def __init__(self, strategy: FillAlgorithm) -> None:
        self.strategy = strategy

    def resize(self, img_file: Path, size: _SIZE) -> Image:
        return self.strategy.make_background(img_file, size)


def main() -> None:
    image_file = Path.cwd() / "behavioral_patterns/strategy_pattern/strategyex/test.png"
    tiled_desktop = Resizer(TiledStrategy())
    tiled_image = tiled_desktop.resize(image_file, (1920, 1080))
    tiled_image.show()


if __name__ == "__main__":
    main()
