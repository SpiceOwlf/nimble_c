import asyncio
import cv2

async def graceful_shutdown(pc, channels=None, ball_manager=None, other_resources=None):
    try:
        if channels:
            for channel in channels:
                if channel and channel.readyState != "closed":
                    channel.close()
                    print(f"Closed channel: {channel.label}")
        
        if ball_manager:
            ball_manager.stop()
            print("Stopped ball manager")
        
        if pc and pc.connectionState != "closed":
            await pc.close()
            print("Closed peer connection")
        
        if other_resources:
            for resource in other_resources:
                if hasattr(resource, 'close'):
                    await resource.close()
                elif hasattr(resource, 'stop'):
                    resource.stop()
        
        cv2.destroyAllWindows()
        
        print("Graceful shutdown completed successfully")
    except Exception as e:
        print(f"Error during graceful shutdown: {e}")

async def handle_shutdown(pc, channels=None, ball_manager=None, other_resources=None):
    """
    Handle shutdown signals and perform graceful shutdown.
    
    Args:
        pc (RTCPeerConnection): The peer connection to close
        channels (list): List of data channels to close
        ball_manager (BallManager): Ball manager instance to stop
        other_resources (list): List of other resources to clean up
    """
    try:
        await asyncio.get_event_loop().create_future()
    except KeyboardInterrupt:
        print("\nReceived shutdown signal")
        await graceful_shutdown(pc, channels, ball_manager, other_resources)
    except Exception as e:
        print(f"Error: {e}")
        await graceful_shutdown(pc, channels, ball_manager, other_resources)
    finally:
        await graceful_shutdown(pc, channels, ball_manager, other_resources) 