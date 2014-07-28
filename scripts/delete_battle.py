
import sys
from hashtag_django.models import Battle

def main():
    if len(sys.argv) < 2:
        print "more args"
        return
    bat_id = int(sys.argv[1])
    print bat_id
    bat = Battle.objects.get(id=bat_id)
    bat.left_hashtag.delete()
    bat.right_hashtag.delete()
    bat.delete()

if __name__ == "__main__":
    main()