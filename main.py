from triangles import TriangleManager, BadInput, SavePicFail, BaseTriangleException


def test1():
    try:
        a = TriangleManager(n=2, k=0.25, w=600, h=400, pic_name='pic1')
    except BadInput as exc:
        print('creation fail, reason: {!r}'.format(str(exc)))
        return

    try:
        a.get_picture()
    except SavePicFail as exc:
        print('saving fail, reason: {}'.format(str(exc)))
        return


def test2():
    try:
        a = TriangleManager(n=6, k=0.5, w=1200, h=800, pic_name='pic2')
        a.get_picture()
    except BaseTriangleException as exc:
        print('total exception: {}'.format(str(exc)))
        return


def main():
    test1()
    test2()


if __name__ == '__main__':
    main()
