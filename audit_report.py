from audit import log_action
from report import generate_report

def main():
    # Simulated end-to-end run for quick demo video
    log_action("SYSTEM_STARTED", {"note": "Prototype started"})
    log_action("INGEST", {"source": "sample_input.pcap", "mode": "replay"})
    log_action("DETECTION", {"alerts_generated": 3, "threshold": 0.80})
    log_action("EVIDENCE_HASHED", {"file": "sample_input.pcap", "sha256": "demo-only"})
    log_action("RUN_COMPLETED", {"status": "success"})

    generate_report()

if __name__ == "__main__":
    main()
