import AppKit
import Foundation

let arguments = Array(CommandLine.arguments.dropFirst())
guard arguments.count >= 2 else {
    fputs("Usage: swift create-image-contact-sheet.swift output.png input1.png ...\n", stderr)
    exit(2)
}

let output = arguments[0]
let inputs = Array(arguments.dropFirst())
let columns = 4
let cellWidth = 360
let previewHeight = 230
let labelHeight = 54
let cellHeight = previewHeight + labelHeight
let rows = Int(ceil(Double(inputs.count) / Double(columns)))
let size = NSSize(width: columns * cellWidth, height: rows * cellHeight)

let canvas = NSImage(size: size)
canvas.lockFocus()
NSColor(calibratedWhite: 0.96, alpha: 1).setFill()
NSBezierPath(rect: NSRect(origin: .zero, size: size)).fill()

let attributes: [NSAttributedString.Key: Any] = [
    .font: NSFont.systemFont(ofSize: 15, weight: .medium),
    .foregroundColor: NSColor(calibratedWhite: 0.16, alpha: 1),
]

for (index, path) in inputs.enumerated() {
    guard let image = NSImage(contentsOfFile: path) else { continue }
    let column = index % columns
    let row = index / columns
    let originX = column * cellWidth
    let originY = Int(size.height) - (row + 1) * cellHeight
    let preview = NSRect(x: originX + 8, y: originY + labelHeight + 8, width: cellWidth - 16, height: previewHeight - 16)
    let scale = min(preview.width / image.size.width, preview.height / image.size.height)
    let drawSize = NSSize(width: image.size.width * scale, height: image.size.height * scale)
    let drawRect = NSRect(x: preview.midX - drawSize.width / 2, y: preview.midY - drawSize.height / 2, width: drawSize.width, height: drawSize.height)
    image.draw(in: drawRect)

    let label = URL(fileURLWithPath: path).lastPathComponent as NSString
    label.draw(in: NSRect(x: originX + 12, y: originY + 12, width: cellWidth - 24, height: labelHeight - 16), withAttributes: attributes)
}

canvas.unlockFocus()
guard let data = canvas.tiffRepresentation,
      let bitmap = NSBitmapImageRep(data: data),
      let png = bitmap.representation(using: .png, properties: [:]) else {
    fputs("Unable to create PNG\n", stderr)
    exit(1)
}
try png.write(to: URL(fileURLWithPath: output))
