"""Do To application.
Main control structure.
"""
import doto


class DoToApp(object):
    
    def load(self):
        """Initial loading screen, user selects where to load/save data.
        """
        self.clear_screen()
        print "Welcome to Do To! What is your name?"
        name = raw_input("> ")

        # if this is a new user, prompt create a new user?
        self.main(name)



    def main(self, user):
        # display first collection in the master_collection
        # control/navigation at bottom

    def clear_screen(self, user=""):
        """Clear screen, return cursor to top left, and display banner.
        Thanks to Graham King http://www.darkcoding.net for code snippet
        """
        sys.stdout.write('\033[2J')
        sys.stdout.write('\033[H')
        sys.stdout.flush()
        print "\n\t\tDo To - %s\n\n" % user


# bootstrap DoTo application
app = DoToApp()
app.load()