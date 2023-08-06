

from mcrcon import MCRcon


# with MCRcon("0.0.0.0", "factory") as mcr:
#     resp = mcr.command("/version")
#     print(resp)



#/silent-command game.write_file("stats.txt", serpent.block(game.forces.player.item_production_statistics.output_counts))

write_stats_command = "/silent-command game.write_file(\"stats.txt\", serpent.block(game.forces.player.item_production_statistics.output_counts))"



def get_stats():
    mcr = MCRcon("0.0.0.0", "factory")
    mcr.connect()
    resp = mcr.command(write_stats_command)
    #do something with the response
    mcr.disconnect()
    return resp




def main():
    print("Factocli RCON Client Started")
    print("Connecting to RCON Address")
    mcr = MCRcon("0.0.0.0", "factory")
    mcr.connect()
    resp = mcr.command(write_stats_command)
    print("Sending command...")
    print("Response: "+resp)
    print("Disconnecting...")
    mcr.disconnect()
    print("Done")





if __name__ == "__main__":
    main()